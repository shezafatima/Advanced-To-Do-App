'use client';

import React, { useState } from 'react';
import { formatRRule, getRecurrenceDescription, RecurrenceRule } from '@/utils/recurrence';

interface RecurrencePickerProps {
  value: string;
  onChange: (rrule: string) => void;
  className?: string;
}

const RecurrencePicker: React.FC<RecurrencePickerProps> = ({ value, onChange, className = '' }) => {
  const [freq, setFreq] = useState<'DAILY' | 'WEEKLY' | 'MONTHLY'>(
    value.includes('DAILY') ? 'DAILY' :
    value.includes('WEEKLY') ? 'WEEKLY' :
    value.includes('MONTHLY') ? 'MONTHLY' : 'DAILY'
  );

  const [interval, setInterval] = useState<number>(() => {
    const match = value.match(/INTERVAL=(\d+)/);
    return match ? parseInt(match[1]) : 1;
  });

  const [ends, setEnds] = useState<'never' | 'after' | 'on'>(
    value.includes('COUNT=') ? 'after' :
    value.includes('UNTIL=') ? 'on' : 'never'
  );

  const [count, setCount] = useState<number>(() => {
    const match = value.match(/COUNT=(\d+)/);
    return match ? parseInt(match[1]) : 10;
  });

  const [endDate, setEndDate] = useState<string>(() => {
    const match = value.match(/UNTIL=(\d{8})/);
    if (match) {
      // Convert YYYYMMDD to YYYY-MM-DD format
      const dateStr = match[1];
      return `${dateStr.substring(0, 4)}-${dateStr.substring(4, 6)}-${dateStr.substring(6, 8)}`;
    }
    return '';
  });

  // Update the rrule when any of the values change
  React.useEffect(() => {
    const rule: RecurrenceRule = {
      freq,
      interval: interval > 1 ? interval : undefined
    };

    if (ends === 'after') {
      rule.count = count;
    } else if (ends === 'on' && endDate) {
      // Convert date to YYYYMMDD format for rrule
      const formattedDate = endDate.replace(/-/g, '');
      rule.until = formattedDate;
    }

    const newRrule = formatRRule(rule);
    onChange(newRrule);
  }, [freq, interval, ends, count, endDate, onChange]);

  const handleFreqChange = (newFreq: 'DAILY' | 'WEEKLY' | 'MONTHLY') => {
    setFreq(newFreq);
  };

  const handleIntervalChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newInterval = Math.max(1, parseInt(e.target.value) || 1);
    setInterval(newInterval);
  };

  return (
    <div className={`space-y-3 ${className}`}>
      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          onClick={() => handleFreqChange('DAILY')}
          className={`px-3 py-1.5 text-sm rounded-md ${
            freq === 'DAILY'
              ? 'bg-purple-600 text-white'
              : 'bg-white/10 text-gray-300 hover:bg-white/20'
          }`}
        >
          Daily
        </button>
        <button
          type="button"
          onClick={() => handleFreqChange('WEEKLY')}
          className={`px-3 py-1.5 text-sm rounded-md ${
            freq === 'WEEKLY'
              ? 'bg-purple-600 text-white'
              : 'bg-white/10 text-gray-300 hover:bg-white/20'
          }`}
        >
          Weekly
        </button>
        <button
          type="button"
          onClick={() => handleFreqChange('MONTHLY')}
          className={`px-3 py-1.5 text-sm rounded-md ${
            freq === 'MONTHLY'
              ? 'bg-purple-600 text-white'
              : 'bg-white/10 text-gray-300 hover:bg-white/20'
          }`}
        >
          Monthly
        </button>
      </div>

      <div className="flex items-center gap-2">
        <span className="text-sm text-gray-300">Every</span>
        <input
          type="number"
          min="1"
          value={interval}
          onChange={handleIntervalChange}
          className="w-16 px-2 py-1.5 bg-white/10 border border-white/20 rounded text-white text-sm"
        />
        <span className="text-sm text-gray-300">
          {freq === 'DAILY' ? 'day(s)' : freq === 'WEEKLY' ? 'week(s)' : 'month(s)'}
        </span>
      </div>

      <div className="pt-2 border-t border-white/10">
        <div className="text-sm text-gray-300 mb-2">Ends:</div>
        <div className="space-y-2">
          <label className="flex items-center">
            <input
              type="radio"
              name="ends"
              checked={ends === 'never'}
              onChange={() => setEnds('never')}
              className="mr-2 text-purple-600 focus:ring-purple-500"
            />
            <span className="text-sm text-gray-300">Never</span>
          </label>

          <label className="flex items-center">
            <input
              type="radio"
              name="ends"
              checked={ends === 'after'}
              onChange={() => setEnds('after')}
              className="mr-2 text-purple-600 focus:ring-purple-500"
            />
            <span className="text-sm text-gray-300">After</span>
            <input
              type="number"
              min="1"
              value={ends === 'after' ? count : 10}
              onChange={(e) => setCount(Math.max(1, parseInt(e.target.value) || 10))}
              disabled={ends !== 'after'}
              className="mx-2 w-16 px-2 py-1 bg-white/10 border border-white/20 rounded text-white text-sm disabled:opacity-50"
            />
            <span className="text-sm text-gray-300">occurrences</span>
          </label>

          <label className="flex items-center">
            <input
              type="radio"
              name="ends"
              checked={ends === 'on'}
              onChange={() => setEnds('on')}
              className="mr-2 text-purple-600 focus:ring-purple-500"
            />
            <span className="text-sm text-gray-300">On</span>
            <input
              type="date"
              value={ends === 'on' ? endDate : ''}
              onChange={(e) => setEndDate(e.target.value)}
              disabled={ends !== 'on'}
              className="ml-2 px-2 py-1 bg-white/10 border border-white/20 rounded text-white text-sm disabled:opacity-50"
            />
          </label>
        </div>
      </div>

      {value && (
        <div className="pt-2 border-t border-white/10">
          <div className="text-xs text-gray-400">Preview: {getRecurrenceDescription(value)}</div>
        </div>
      )}
    </div>
  );
};

export default RecurrencePicker;