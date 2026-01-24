'use client';

import React, { useState, useEffect } from 'react';
import { useTheme } from '@/context/ThemeContext';
import { useNotification } from '@/context/NotificationContext';
import { useAuth } from '@/context/auth-context';
import { UserProfile, UpdateProfileRequest } from '@/types/todo';
import { profileService } from '@/services/api';

const ProfilePage: React.FC = () => {
  const { theme, setTheme } = useTheme();
  const { showSuccess, showError } = useNotification();
  const { user } = useAuth();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [editing, setEditing] = useState<boolean>(false);
  const [formData, setFormData] = useState<UpdateProfileRequest>({
    displayName: '',
    preferredLanguage: 'en',
    notificationPreferences: {
      toastNotifications: true,
      emailReminders: false,
    },
    avatar: ''
  });

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      const response = await profileService.getProfile();
      const profileData = response.data as UserProfile;

      setProfile(profileData);
      setFormData({
        displayName: profileData.displayName,
        preferredLanguage: profileData.preferredLanguage,
        themePreference: profileData.themePreference || 'dark',
        notificationPreferences: profileData.notificationPreferences,
        avatar: profileData.avatar || ''
      });
    } catch (error) {
      console.error('Error fetching profile:', error);
      // Create a default profile if none exists
      const defaultProfile: UserProfile = {
        id: 'default-id',
        userId: 'current-user-id',
        displayName: 'New User',
        preferredLanguage: 'en',
        themePreference: 'dark',
        notificationPreferences: {
          toastNotifications: true,
          emailReminders: false,
        },
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      setProfile(defaultProfile);
      setFormData({
        displayName: defaultProfile.displayName,
        preferredLanguage: defaultProfile.preferredLanguage,
        themePreference: defaultProfile.themePreference || 'dark',
        notificationPreferences: defaultProfile.notificationPreferences,
        avatar: defaultProfile.avatar || ''
      });

      showError('Using default profile settings');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    if (name.startsWith('notificationPreferences.')) {
      const notificationKey = name.split('.')[1] as keyof typeof formData.notificationPreferences;
      setFormData(prev => {
        const newNotificationPrefs = {
          ...prev.notificationPreferences,
          [notificationKey]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
        };

        // Ensure required boolean fields are always present
        return {
          ...prev,
          notificationPreferences: {
            toastNotifications: !!newNotificationPrefs.toastNotifications,
            emailReminders: !!newNotificationPrefs.emailReminders,
            ...newNotificationPrefs
          }
        };
      });
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  // Special handler for theme changes
  const handleThemeChange = (newTheme: string) => {
    setFormData(prev => ({
      ...prev,
      themePreference: newTheme
    }));
    setTheme(newTheme as 'light' | 'dark' | 'auto');
  };

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = e.target;
    if (name.startsWith('notificationPreferences.')) {
      const notificationKey = name.split('.')[1] as keyof typeof formData.notificationPreferences;
      setFormData(prev => {
        const newNotificationPrefs = {
          ...prev.notificationPreferences,
          [notificationKey]: checked
        };

        // Ensure required boolean fields are always present
        return {
          ...prev,
          notificationPreferences: {
            toastNotifications: !!newNotificationPrefs.toastNotifications,
            emailReminders: !!newNotificationPrefs.emailReminders,
            ...newNotificationPrefs
          }
        };
      });
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: checked
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      // Prepare the data to send, handling avatar conversion if needed
      const profileDataToSend = {
        ...formData,
        // Convert avatar from base64 to binary if it's a data URL
        avatar: formData.avatar?.startsWith('data:') ? formData.avatar : undefined,
        // Ensure theme preference is included
        themePreference: formData.themePreference || theme
      };

      const response = await profileService.updateProfile(profileDataToSend);
      const updatedProfile = response.data as UserProfile;

      setProfile(updatedProfile);
      showSuccess('Profile updated successfully!');
      setEditing(false);
    } catch (error) {
      console.error('Error updating profile:', error);
      showError('Failed to update profile');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-4 sm:p-6">
      <h1 className="text-3xl font-bold text-gray-200 mb-8">Profile Settings</h1>

      <div className="bg-white/10 backdrop-blur-sm rounded-xl border border-white/20 p-6 shadow-lg">
        <div className="flex flex-col md:flex-row gap-8">
          {/* Avatar Section */}
          <div className="flex flex-col items-center md:items-start">
            {profile?.avatar ? (
              <img
                src={typeof profile.avatar === 'string' && profile.avatar.startsWith('data:') ?
                  profile.avatar :
                  `data:image/jpeg;base64,${profile.avatar}`
                }
                alt="Avatar"
                className="w-32 h-32 rounded-full mb-4 object-cover border-4 border-white/20"
              />
            ) : (
              <div className="w-32 h-32 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white text-4xl font-bold mb-4 overflow-hidden">
                {(profile?.displayName && profile.displayName.charAt(0)) || 'U'}
              </div>
            )}
            <label className="px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-lg hover:from-purple-700 hover:to-indigo-700 transition-all cursor-pointer">
              Change Avatar
              <input
                type="file"
                className="hidden"
                accept="image/*"
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    const file = e.target.files[0];
                    // Validate file type and size
                    if (!file.type.match('image.*')) {
                      showError('Please select an image file');
                      return;
                    }
                    if (file.size > 2 * 1024 * 1024) { // 2MB limit
                      showError('Image size must be less than 2MB');
                      return;
                    }

                    // Convert to base64 for submission
                    const reader = new FileReader();
                    reader.onload = (event) => {
                      if (event.target?.result) {
                        setFormData(prev => ({
                          ...prev,
                          avatar: event.target?.result as string
                        }));
                      }
                    };
                    reader.readAsDataURL(file);
                  }
                }}
              />
            </label>
          </div>

          {/* Profile Details */}
          <div className="flex-1">
            {editing ? (
              <form onSubmit={handleSubmit}>
                <div className="space-y-6">
                  <div>
                    <label htmlFor="displayName" className="block text-sm font-medium text-gray-300 mb-1">
                      Display Name
                    </label>
                    <input
                      type="text"
                      id="displayName"
                      name="displayName"
                      value={formData.displayName}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-400"
                      required
                    />
                  </div>

                  <div>
                    <label htmlFor="preferredLanguage" className="block text-sm font-medium text-gray-300 mb-1">
                      Language
                    </label>
                    <select
                      id="preferredLanguage"
                      name="preferredLanguage"
                      value={formData.preferredLanguage}
                      onChange={handleInputChange}
                      className="w-full px-4 py-2.5 bg-white/10 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-800"
                    >
                      <option value="en">English</option>
                    </select>
                  </div>

                  <div>
                    <h3 className="text-lg font-medium text-gray-200 mb-3">Notification Preferences</h3>

                    <div className="space-y-3">
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          id="toastNotifications"
                          name="notificationPreferences.toastNotifications"
                          checked={formData.notificationPreferences?.toastNotifications ?? false}
                          onChange={handleCheckboxChange}
                          className="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-600 rounded bg-transparent"
                        />
                        <label htmlFor="toastNotifications" className="ml-2 block text-sm text-gray-300">
                          Enable toast notifications
                        </label>
                      </div>

                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          id="emailReminders"
                          name="notificationPreferences.emailReminders"
                          checked={formData.notificationPreferences?.emailReminders ?? false}
                          onChange={handleCheckboxChange}
                          className="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-600 rounded bg-transparent"
                        />
                        <label htmlFor="emailReminders" className="ml-2 block text-sm text-gray-300">
                          Email reminders for due tasks
                        </label>
                      </div>
                    </div>
                  </div>

                  <div className="flex space-x-4 pt-4">
                    <button
                      type="submit"
                      className="px-6 py-2.5 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-medium rounded-lg hover:from-green-600 hover:to-emerald-700 transition-all"
                    >
                      Save Changes
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setEditing(false);
                        // Reset form to original values
                        if (profile) {
                          setFormData({
                            displayName: profile.displayName,
                            preferredLanguage: profile.preferredLanguage,
                            themePreference: profile.themePreference || 'dark',
                            notificationPreferences: profile.notificationPreferences,
                            avatar: profile.avatar || ''
                          });
                        }
                      }}
                      className="px-6 py-2.5 bg-gradient-to-r from-gray-600 to-gray-700 text-white font-medium rounded-lg hover:from-gray-700 hover:to-gray-800 transition-all"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </form>
            ) : (
              <div className="space-y-6">
                <div>
                  <h3 className="text-sm font-medium text-gray-400">Display Name</h3>
                  <p className="text-lg text-gray-200">{profile?.displayName}</p>
                </div>

                <div>
                  <h3 className="text-sm font-medium text-gray-400">Email</h3>
                  <p className="text-lg text-gray-200">{user?.email || 'No email available'}</p>
                </div>

                <div>
                  <h3 className="text-sm font-medium text-gray-400">Language</h3>
                  <p className="text-lg text-gray-200">
                    {profile?.preferredLanguage === 'en' ? 'English' : 'English'}
                  </p>
                </div>

                <div>
                  <h3 className="text-sm font-medium text-gray-400">Theme</h3>
                  <p className="text-lg text-gray-200 capitalize">{theme}</p>
                  <div className="mt-2 flex space-x-2">
                    {(['light', 'dark', 'auto'] as const).map((t) => (
                      <button
                        key={t}
                        onClick={() => handleThemeChange(t)}
                        className={`px-3 py-1.5 rounded-md text-sm font-medium ${
                          theme === t
                            ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                            : 'bg-white/10 text-gray-300 hover:bg-white/20'
                        }`}
                      >
                        {t.charAt(0).toUpperCase() + t.slice(1)}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="text-sm font-medium text-gray-400">Notification Preferences</h3>
                  <ul className="mt-2 space-y-2">
                    <li className="flex items-center">
                      <span className={`w-3 h-3 rounded-full mr-2 ${profile?.notificationPreferences.toastNotifications ? 'bg-green-500' : 'bg-red-500'}`}></span>
                      <span className="text-gray-300">Toast notifications: {profile?.notificationPreferences.toastNotifications ? 'Enabled' : 'Disabled'}</span>
                    </li>
                    <li className="flex items-center">
                      <span className={`w-3 h-3 rounded-full mr-2 ${profile?.notificationPreferences.emailReminders ? 'bg-green-500' : 'bg-red-500'}`}></span>
                      <span className="text-gray-300">Email reminders: {profile?.notificationPreferences.emailReminders ? 'Enabled' : 'Disabled'}</span>
                    </li>
                  </ul>
                </div>

                <button
                  onClick={() => setEditing(true)}
                  className="mt-4 px-6 py-2.5 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-medium rounded-lg hover:from-purple-700 hover:to-indigo-700 transition-all"
                >
                  Edit Profile
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;