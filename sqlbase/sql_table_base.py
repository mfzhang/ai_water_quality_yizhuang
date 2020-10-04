from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class QualityIndicator(Base):
    __tablename__ = 'quality_indicator_1'
    timestamp = Column(Integer, primary_key=True)
    value1 = Column(Integer)
    value2 = Column(Integer)
    status = Column(String)

    def __repr__(self):
        return "<QualityIndicator(timestamp={}, value1={}, value2={}, status={})>".format(
            self.timestamp,
            self.value1,
            self.value2,
            self.status
        )


INDICATOR_LIST = [
    QualityIndicator
]


def test():
    print('---- start -------')
    engine = create_engine(r'sqlite:///C:\Users\Admin\PycharmProjects\ai_water_plant\sqlbase\foo.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    sample1 = QualityIndicator(timestamp=int(datetime.now().timestamp()),
                               value1=1,
                               value2=1,
                               status='ok')
    session.add(sample1)
    session.commit()
    print('---- end ----')


if __name__ == '__main__':
    test()
