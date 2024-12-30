from itemadapter import ItemAdapter
from .database.base import DatabaseManager
from .database.models import Hotel


class PostgresPipeline:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.db_manager = DatabaseManager()


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            connection_string=crawler.settings.get('SQLALCHEMY_CONNECTION_STRING')
        )


    def open_spider(self, spider):
        self.db_manager.initialize(self.connection_string)
        self.db_manager.create_tables()


    def process_item(self, item, spider):
        session = self.db_manager.get_session()
        try:
            item_dict = dict(item)
            hotel = Hotel(
                city_name=item_dict.get('city_name'),
                property_title=item_dict.get('property_title'),
                hotel_id=item_dict.get('hotel_id'),
                price=item_dict.get('price'),
                rating=item_dict.get('rating'),
                address=item_dict.get('address'),
                latitude=float(item_dict.get('latitude', 0)) if item_dict.get('latitude') else None,
                longitude=float(item_dict.get('longitude', 0)) if item_dict.get('longitude') else None,
                room_type=item_dict.get('room_type'),
                image=item_dict.get('image'),
                local_image_path=item_dict.get('local_image_path')
            )
            session.add(hotel)
            session.commit()
            spider.logger.info(f"Hotel Added Successfully - 200")
        except Exception as e:
            session.rollback()
            spider.logger.error(e)
        finally:
            session.close()
        return item