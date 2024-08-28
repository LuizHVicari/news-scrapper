import requests
from decouple import config
from loguru import logger
from typing import List, TypedDict
from datetime import datetime


AZURE_API_KEY = config('AZURE_KEY', cast=str)
WEB_SEARCH_ENDPOINT = config('AZURE_SEARCH_ENDPOINT', cast=str)

logger.info(f'api key: {AZURE_API_KEY}')
logger.info(f'endpoint: {WEB_SEARCH_ENDPOINT}')

ResponseDict = TypedDict('ResponseDict', {
    'name': str,
    'description': str | None,
    'url': str,
    'date_published': datetime
})

def get_news_from_query(query: str, 
                        count: int = 50, 
                        offset: int = 0, 
                        mkt: str = 'pt-BR', 
                        freshness: str = 'Day') -> List[ResponseDict] | None:
    params = {
        'q': query,
        'count': count,
        'offset': offset,
        'mkt': mkt,
        'freshness': freshness
    }

    headers = {
    'Ocp-Apim-Subscription-Key': AZURE_API_KEY
    }

    response = requests.get(
        url=WEB_SEARCH_ENDPOINT,
        headers=headers,
        params=params
    )

    logger.debug(response.status_code)

    if response.status_code == 200:
        logger.success(f'Successfully collected news for query {query}')
        values = response.json()['value']

        news = list()
        for value in values:
            response_dict: ResponseDict = dict()
            response_dict['name'] = value['name']
            response_dict['description'] = value.get('description')
            response_dict['url'] = value['url']
            response_dict['date_published'] = datetime.strptime(
                value['datePublished'][:-2], # removes 0Z from timestamp
                '%Y-%m-%dT%H:%M:%S.%f')

            news.append(response_dict)
        return news 

    else:
        logger.warning(f'Could not collect news for query {query}')
        return None


if __name__ == '__main__':
    query = 'openai'
    news = get_news_from_query(query)
    logger.debug(news)