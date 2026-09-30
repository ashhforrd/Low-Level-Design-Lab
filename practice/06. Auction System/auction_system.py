from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional
from uuid import uuid4


class AuctionStatus(Enum):
    DRAFT = auto()
    OPEN = auto()
    CLOSED = auto()


@dataclass(frozen=True)
class Item:
    item_id: str
    item_name: str


@dataclass(frozen=True)
class Bid:
    bidder_id: str
    amount: int

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("Bid amount must be greater than zero")


class Auction:
    def __init__(
            self, 
            auction_id: str, 
            seller_id: str, 
            item: Item, 
            starting_price: int, 
            ) -> None:

        if starting_price <= 0:
            raise ValueError("Starting price must be greater than zero")
        
        self.auction_id = auction_id
        self.seller_id = seller_id
        self.item = item
        self.starting_price = starting_price
        self.status = AuctionStatus.DRAFT
        self.bids: list[Bid] = []

    def open(self, seller_id: str) -> None:
        if seller_id != self.seller_id:
            raise ValueError("Seller ID must be the same as auction owner")
        
        if self.status != AuctionStatus.DRAFT:
            raise ValueError("Only DRAFT status auction can be opened")

        self.status = AuctionStatus.OPEN

    def get_highest_bid(self) -> Optional[Bid]:
        if not self.bids:
            return None

        return self.bids[-1]

    def place_bid(self, bidder_id: str, amount: int) -> Bid:
        if self.status != AuctionStatus.OPEN:
            raise ValueError("Auction is not opening")

        if bidder_id == self.seller_id:
            raise ValueError("Cannot place a bid into your own auction")

        highest_bid = self.get_highest_bid()

        if highest_bid is not None:
            if amount <= highest_bid.amount:
                raise ValueError("Bid amount must be greater than the highest bid")
        else:
            if amount < self.starting_price:
                raise ValueError("First bid must be at least the starting price")

        bid = Bid(bidder_id, amount)

        self.bids.append(bid)

        return bid

    def close(self, seller_id: str) -> Optional[Bid]:
        if seller_id != self.seller_id:
            raise ValueError("Cannot close auction")

        if self.status != AuctionStatus.OPEN:
            raise ValueError("Cannot close auction")

        self.status = AuctionStatus.CLOSED

        return self.get_highest_bid()


class AuctionSystem:
    def __init__(self) -> None:
        self.auctions: dict[str, Auction] = {}

    def create_auction(
            self,
            seller_id: str,
            item: Item,
            starting_price: int
    ) -> Auction:
        auction_id = str(uuid4())

        auction = Auction(
            auction_id,
            seller_id,
            item,
            starting_price,
        )

        self.auctions[auction_id] = auction

        return auction

    def get_auction(self, auction_id: str) -> Auction:
        auction = self.auctions.get(auction_id)

        if auction is None:
            raise ValueError("Auction not found")
        
        return auction

    def open_auction(self, auction_id: str, seller_id: str) -> None:
        auction = self.get_auction(auction_id)
        auction.open(seller_id)

    def place_bid(self, auction_id: str, bidder_id: str, amount: int) -> Bid:
        auction = self.get_auction(auction_id)
        return auction.place_bid(bidder_id, amount)

    def close_auction(self, auction_id: str, seller_id: str) -> Optional[Bid]:
        auction = self.get_auction(auction_id)
        return auction.close(seller_id)


def main() -> None:
    system = AuctionSystem()

    item = Item(
        item_id="ITEM-1",
        item_name="Mechanical Keyboard",
    )

    auction = system.create_auction(
        seller_id="SELLER-1",
        item=item,
        starting_price=500_000,
    )

    print("Initial status:", auction.status)

    system.open_auction(
        auction.auction_id,
        "SELLER-1",
    )

    print("Opened status:", auction.status)

    first_bid = system.place_bid(
        auction.auction_id,
        bidder_id="BIDDER-1",
        amount=500_000,
    )

    print("First bid:", first_bid)

    second_bid = system.place_bid(
        auction.auction_id,
        bidder_id="BIDDER-2",
        amount=600_000,
    )

    print("Second bid:", second_bid)

    try:
        system.place_bid(
            auction.auction_id,
            bidder_id="BIDDER-3",
            amount=550_000,
        )
    except ValueError as error:
        print("Rejected bid:", error)

    winning_bid = system.close_auction(
        auction.auction_id,
        "SELLER-1",
    )

    print("Final status:", auction.status)
    print("Winner:", winning_bid.bidder_id)
    print("Winning amount:", winning_bid.amount)

    try:
        system.place_bid(
            auction.auction_id,
            bidder_id="BIDDER-3",
            amount=700_000,
        )
    except ValueError as error:
        print("Bid after close rejected:", error)


if __name__ == "__main__":
    main()