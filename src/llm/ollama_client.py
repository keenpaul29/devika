import ollama
from src.logger import Logger
from src.config import Config

log = Logger()


class Ollama:
    def __init__(self):
        try:
            self.client = ollama.Client(Config().get_ollama_api_endpoint())
            # Validate client connection and get models
            response = self.client.list()
            if not response or 'models' not in response:
                raise Exception("Invalid response from Ollama server")
            
            # Extract models from response
            self.models = response.get("models", [])
            if not isinstance(self.models, list):
                raise Exception("Invalid models format from Ollama server")
            
            # Check if deepseek-r1:7b is available
            if not any(model.get('name', '').startswith('deepseek-r1:7b') for model in self.models):
                log.info("Pulling deepseek-r1:7b model...")
                self.client.pull('deepseek-r1:7b')
                response = self.client.list()
                if response and 'models' in response:
                    self.models = response.get("models", [])
            
            # Extract model names more reliably
            model_names = []
            for model in self.models:
                name = model.get('name', '')
                if ':' in name:  # Handle format like 'deepseek-r1:7b'
                    name = name.split(':')[0] + ':' + name.split(':')[1]
                model_names.append(name)
            
            log.info("Ollama available with models: " + ", ".join(model_names))
        except Exception as e:
            self.client = None
            log.warning(f"Ollama not available: {str(e)}")
            log.warning("Please ensure the Ollama server is running and accessible at " + Config().get_ollama_api_endpoint())


    def inference(self, model_id: str, prompt: str) -> str:
        response = self.client.generate(
            model=model_id,
            prompt=prompt.strip(),
            options={"temperature": 0}
        )
        return response['response']
