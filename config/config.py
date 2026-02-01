import os
from dotenv import load_dotenv

# Load .env file variables into os.environ
load_dotenv()

class Config:
    # Default to STAGING if not set
    ENV = os.getenv("TEST_ENV", "STAGING").upper()

    @property
    def BASE_URL(self):
        if self.ENV == "DEV":
            return os.getenv("DEV_BASE_URL")
        elif self.ENV == "PROD":
            return os.getenv("PROD_BASE_URL")
        return os.getenv("STAGING_BASE_URL")

    @property
    def USERNAME(self):
        if self.ENV == "PROD":
            return os.getenv("PROD_USERNAME")
        return os.getenv(f"{self.ENV}_USERNAME") or os.getenv("COMMON_USERNAME")

    @property
    def PASSWORD(self):
        if self.ENV == "PROD":
            return os.getenv("PROD_PASSWORD")
        return os.getenv(f"{self.ENV}_PASSWORD") or os.getenv("COMMON_PASSWORD")

# Create a global instance to be imported
config = Config()