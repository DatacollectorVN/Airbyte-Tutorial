from airbyte_cdk.sources.streams.http import HttpStream
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple
import requests


class Pokemon(HttpStream):
    url_base = "https://pokeapi.co/api/v2/"

    # Set is as default for streams API
    primary_key = None

    def __init__(self, pokemon_name: str, **kwargs):
        super().__init__(**kwargs)
        self.pokemon_name = pokemon_name
    
    def path(self, **kwargs) -> str:
        pokemon_name = self.pokemon_name
        # This defines the path to the endpoint that we want to hit.
        return f"pokemon/{pokemon_name}"
    
    def request_params(
            self,
            stream_state: Mapping[str, Any],
            stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None,
    ) -> MutableMapping[str, Any]:
        # The api requires that we include the Pokemon name as a query param so we do that in this method.
        return {"pokemon_name": self.pokemon_name}

    def parse_response(
            self,
            response: requests.Response,
            stream_state: Mapping[str, Any],
            stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly,
        # so we just return a list containing the response.
        return [response.json()]

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # While the PokeAPI does offer pagination, we will only ever retrieve one Pokemon with this implementation,
        # so we just return None to indicate that there will never be any more pages in the response.
        return None