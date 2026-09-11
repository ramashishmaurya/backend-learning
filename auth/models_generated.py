from typing import Optional
import datetime
import decimal

from sqlalchemy import Date, Integer, Numeric, PrimaryKeyConstraint, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = 'department'
    __table_args__ = (
        PrimaryKeyConstraint('department_id', name='department_pkey'),
    )

    department_id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    department_name: Mapped[Optional[str]] = mapped_column(String(50))


class Employee(Base):
    __tablename__ = 'employee'
    __table_args__ = (
        PrimaryKeyConstraint('emp_id', name='employee_pkey'),
    )

    emp_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(50))
    department_id: Mapped[Optional[int]] = mapped_column(Integer)


class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        PrimaryKeyConstraint('order_id', name='orders_pkey'),
    )

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    product_id: Mapped[Optional[int]] = mapped_column(Integer)
    order_status: Mapped[Optional[str]] = mapped_column(String(50))
    sales: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))


class Project(Base):
    __tablename__ = 'project'
    __table_args__ = (
        PrimaryKeyConstraint('project_id', name='project_pkey'),
    )

    project_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_name: Mapped[Optional[str]] = mapped_column(String(50))
    emp_id: Mapped[Optional[int]] = mapped_column(Integer)


class Sales(Base):
    __tablename__ = 'sales'
    __table_args__ = (
        PrimaryKeyConstraint('sale_id', name='sales_pkey'),
    )

    sale_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_name: Mapped[Optional[str]] = mapped_column(String(100))
    product: Mapped[Optional[str]] = mapped_column(String(100))
    quantity: Mapped[Optional[int]] = mapped_column(Integer)
    price: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    sale_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

