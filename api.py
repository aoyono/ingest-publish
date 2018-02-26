# -*- coding: utf-8 -*-
"""
The web app that publishes a unique endpoint to get product information by id
"""
from flask import Flask, Response, jsonify

app = Flask(__name__)


@app.route('/products/<product_id>')
def serve_product(product_id):
    for product in getattr(app, 'products_storage', []):
        if product['id'] == product_id:
            return jsonify(product)
    return Response('Not Found', status=404)
