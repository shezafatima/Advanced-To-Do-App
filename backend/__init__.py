from pathlib import Path
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))