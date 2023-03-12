from .database import (
    COLUMN,
    Model,
    SurrogatePK,
    db,
    reference_col,
    RELATIONSHIP
)


class Customers(SurrogatePK, Model):
    """
    Model for customers table
    """
    __tablename__ = 'customers'
    name = COLUMN(db.String(96), nullable=False)
    regist = COLUMN(db.DateTime, nullable=False)
    birth = COLUMN(db.DateTime, nullable=False)
    personal_info = COLUMN(db.Integer(), nullable=False)
    gender = COLUMN(db.String(1))
    photo = COLUMN(db.VARBINARY)

    def __repr__(self):
        return f'Name: {self.name} | Register: {self.regist}'
    
    def sum_purchases(self):
        sum = 0
        for item in self.purchases:
            sum += item.sum()
        return sum

    def to_dict(self):
        return {
            'user_id': self.id,
            'name': self.name,
            'regist': self.regist,
            'birth': self.birth,
            'personal_info': self.personal_info,
            'gender': self.gender,
            'photo': self.photo
        }


class Products(SurrogatePK, Model):
    """
    Model for products table
    """
    __tablename__ = 'products'
    name = COLUMN(db.String(96), nullable=False)
    purchase_price = COLUMN(db.Integer(), nullable=False)
    sell_price = COLUMN(db.Integer(), nullable=False)


class Purchases(SurrogatePK, Model):
    """
    Model for purchases table
    """
    __tablename__ = 'purchases'
    count = COLUMN(db.Integer(), nullable=False)
    date = COLUMN(db.DateTime, nullable=False)
    customer_id = reference_col('customers', nullable=True)
    customer = RELATIONSHIP('Customers', backref='purchases')
    product_id = reference_col('products', nullable=True)
    product = RELATIONSHIP('Products', backref='purchases')

    def sum(self):
        return self.count*self.product.sell_price

    def __repr__(self):
        return (
            f'data: {self.date} | '
            f'customer: {self.customer.name} | '
            f'product: {self.product.name} | '
            f'count: {self.count} | '
            f'cost: {self.product.sell_price} | '
            f'sum: {self.sum()}'
        )
