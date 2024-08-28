from celery import shared_task
from loguru import logger
from decouple import config
from django.core.exceptions import ValidationError

from apps.news.models import Query, News
from apis import get_news_from_query


def get_news() -> list[News]:
    queries_id = Query.objects.all().values('id')

    for q_id in queries_id:
        query: Query = Query.objects.get(id=q_id['id'])
        news = get_news_from_query(
            query=query.query_term,
            count=query.count,
            offset=query.offset,
            mkt=query.mkt,
            freshness=query.freshness
        )

        returning_news = list()
        for n in news:
            try:
                n_obj = News()
                for k, v in n.items():
                    setattr(n_obj, k, v)
                n_obj.full_clean()
                n_obj.save()
                logger.success(f'Saved news to database')
                returning_news.append(n_obj)

            except ValidationError as e:
                logger.warning(f'Could not save news since error {str(e)} happened')
    return returning_news
