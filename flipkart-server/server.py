from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from flask_cors import CORS
from flask import Flask, request, jsonify, current_app
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scraped_data2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(50), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    size = db.Column(db.String(20), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    product_image = db.Column(db.String(200), nullable=True)
    scraped_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Listing {self.title}>"

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "mobile_number": self.mobile_number,
            "size": self.size,
            "category": self.category,
            "product_image": self.product_image,
            "scraped_at": self.scraped_at.strftime('%Y-%m-%d %H:%M:%S')
        }


def scrape_listing(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        try:
            title = soup.find('span', {'class': 'G6XhRU'}).text
        except AttributeError:
            title = "Title not Found"

        try:
            description = soup.find('span', {'class': 'B_NuCI'}).text
        except AttributeError:
            description = "Description not Found"

        try:
            price = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).text
        except AttributeError:
            price = "Price not Found"

        try:
            mobile_number = soup.find('div', {'class': '_3LWZlK _3uSWvT'}).text
        except AttributeError:
            mobile_number = "Price not Found"

        try:
            size = soup.find('span', {'class': '_1rcQuH _3DM78Z'}).text
        except AttributeError:
            size = "Size not Found"

        second_anchor_tag = soup.find_all('a', {'class': '_2whKao'})
        try:
            category = second_anchor_tag[1].text if len(second_anchor_tag) > 1 else 'Not Able to Fetch'
        except IndexError:
            category = "Category not Found"
        try:
            product_image = soup.find('img', {'class': '_2r_T1I _396QI4'}).get('src') if soup.find('img', {'class': '_2r_T1I _396QI4'}) else None
        except AttributeError:
            product_image = "Element not Found"

        return title, description, price, mobile_number, size, category, product_image

    return None, None, None, None, None, None, None


@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL not provided'}), 400

    # Check if the data is already present in the database
    listing = Listing.query.filter_by(url=url).first()

    # If data is not present or it is older than a week, scrape and update
    if not listing or datetime.utcnow() - listing.scraped_at > timedelta(days=7):
        title, description, price, mobile_number, size, category, product_image = scrape_listing(url)
        if title and description and price and mobile_number:
            if not listing:
                listing = Listing(url=url, title=title, description=description,
                                  price=price, mobile_number=mobile_number,
                                  size=size, category=category, product_image=product_image)
                db.session.add(listing)
            else:
                listing.title = title
                listing.description = description
                listing.price = price
                listing.mobile_number = mobile_number
                listing.size = size
                listing.category = category
                listing.product_image = product_image

            listing.scraped_at = datetime.utcnow()
            db.session.commit()

    return jsonify(listing.serialize())

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(Listing.category).distinct().all()
    categories = [category[0] for category in categories]
    return jsonify(categories)

@app.route('/scraped-urls', methods=['GET'])
def get_scraped_urls_by_category():
    category = request.args.get('category')
    if not category:
        return jsonify({'error': 'Category not provided'}), 400

    listings = Listing.query.filter_by(category=category).all()
    scraped_data = [{
        'url': listing.url,
        'scraped_at': listing.scraped_at.strftime('%Y-%m-%d %H:%M:%S')
    } for listing in listings]

    return jsonify(scraped_data)


@app.route('/listings', methods=['GET'])
def get_listings():
    listings = Listing.query.all()
    return jsonify([listing.serialize() for listing in listings])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
