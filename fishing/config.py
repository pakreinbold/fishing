import os


class Environment:
    @staticmethod
    def _get_env_var(var_name: str, default: str | None = None) -> str | None:
        env_var = os.getenv(var_name)
        if env_var == '':
            print(f"No ENV var found for {var_name}, returning default: {default}")
            return default
        else:
            return env_var

    @property
    def gcp_project(self) -> str | None:
        return self._get_env_var("GCP_PROJECT_ID")

    @property
    def bq_dataset(self) -> str | None:
        return self._get_env_var("BQ_DATASET")
