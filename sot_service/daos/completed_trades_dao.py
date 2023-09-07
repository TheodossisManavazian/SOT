from sqlalchemy import text
from sqlalchemy.engine import Connection


def insert_new_trade(conn: Connection, request: dict) -> None:
    sql = """
        INSERT INTO jaat.completed_trades(
            symbol,
            quantity,
            bought_price_per_share,
            sold_price_per_share,
            equity,
            realized_gain,
            percent_gain,
            strategy,
            updated_at
        ) VALUES (
            :symbol,
            :quantity,
            :bought_price_per_share,
            :sold_price_per_share,
            :equity,
            :realized_gain,
            :percent_gain,
            :strategy,
            :updated_at
        )
    """
    conn.execute(text(sql), request)
