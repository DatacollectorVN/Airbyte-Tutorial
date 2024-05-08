from airbyte_cdk.sources import AbstractSource
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple
from airbyte_cdk.sources.streams import Stream
from . import constants
from . import streams

import logging
logger = logging.getLogger("airbyte")


# Airbyte Source
class SourcePokemonApi(AbstractSource):
    def check_connection(self, logger, config) -> Tuple[bool, any]:
        """ Implement a `check` operation for the Source. This operation should test whether the Source can connect to the underlying service. 
            It should return a tuple where the first element is a boolean indicating whether the connection was successful, and the second element is an optional error message.
        """

        logger.info("Checking Pokemon API connection...")
        pokemon_name = config["pokemon_name"]
        if self._validate_pokemon_name(pokemon_name):
            error = f"Pokemon {pokemon_name} not found in Pokemon API"
            logger.error(f"PokeAPI connection failed: {error}")
            return False, error
        else:
            logger.info(f"PokeAPI connection success: {pokemon_name} is a valid Pokemon")
            return True, None
    
    def _validate_pokemon_name(sefl, pokemon_name) -> bool:
        # TODO: Implement a function to validate the Pokemon name\
        # For now, we will just return False if the Pokemon name is not in the list of valid Pokemon names
        return pokemon_name not in constants.POKEMON_VALID_NAMES
    
    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        """ Return a list of streams for the Source """
        return [streams.Pokemon(pokemon_name=config["pokemon_name"])]
    