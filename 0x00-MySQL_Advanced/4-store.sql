-- A SQL script that creates a trigger that decreases the quantity of an 
-- item after adding a new order.

/*
    Quantity in the table items can be negative.
    Updating multiple tables for one action from your application can generate issue
    to keep your data in a good shape, let MySQL do it for you!
*/

CREATE TRIGGER Triger_Orders
AFTER INSERT ON orders FOR EACH ROW
    UPDATE items
        SET items.quantity = items.quantity - NEW.number
        WHERE items.name = NEW.item_name;
