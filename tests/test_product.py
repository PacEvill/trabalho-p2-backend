def test_create_product(client):
    """
    Testa a criação de um produto válido. Deve retornar 210 Created e os dados criados.
    """
    response = client.post(
        "/produtos/",
        json={"name": "Teclado Mecânico", "description": "Teclado Switch Blue", "price": 250.0, "stock": 10}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Teclado Mecânico"
    assert "id" in data
    assert data["price"] == 250.0
    assert data["stock"] == 10

def test_create_product_invalid_price(client):
    """
    Testa a criação com preço negativo. Deve falhar com 422 Unprocessable Entity.
    """
    response = client.post(
        "/produtos/",
        json={"name": "Teclado Mecânico", "description": "Preço Inválido", "price": -5.0, "stock": 10}
    )
    assert response.status_code == 422

def test_create_product_invalid_stock(client):
    """
    Testa a criação com estoque negativo. Deve falhar com 422 Unprocessable Entity.
    """
    response = client.post(
        "/produtos/",
        json={"name": "Teclado Mecânico", "description": "Estoque Inválido", "price": 250.0, "stock": -1}
    )
    assert response.status_code == 422

def test_read_product(client):
    """
    Testa a leitura de um produto existente. Deve retornar 200 OK.
    """
    # Cria primeiro
    create_response = client.post(
        "/produtos/",
        json={"name": "Mouse Gamer", "price": 120.0, "stock": 5}
    )
    product_id = create_response.json()["id"]
    
    # Lê em seguida
    response = client.get(f"/produtos/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Mouse Gamer"
    assert data["id"] == product_id

def test_read_product_not_found(client):
    """
    Testa a busca de um produto inexistente. Deve retornar 404 Not Found.
    """
    response = client.get("/produtos/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"

def test_read_all_products(client):
    """
    Testa a listagem de múltiplos produtos. Deve retornar 200 OK.
    """
    client.post("/produtos/", json={"name": "Produto A", "price": 10.0, "stock": 2})
    client.post("/produtos/", json={"name": "Produto B", "price": 20.0, "stock": 4})
    
    response = client.get("/produtos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

def test_update_product(client):
    """
    Testa a atualização completa de um produto existente. Deve retornar 200 OK.
    """
    # Cria primeiro
    create_response = client.post(
        "/produtos/",
        json={"name": "Monitor", "price": 800.0, "stock": 3}
    )
    product_id = create_response.json()["id"]
    
    # Atualiza
    response = client.put(
        f"/produtos/{product_id}",
        json={"name": "Monitor Ultrawide", "description": "IPS 29 polegadas", "price": 950.0, "stock": 5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Monitor Ultrawide"
    assert data["description"] == "IPS 29 polegadas"
    assert data["price"] == 950.0
    assert data["stock"] == 5

def test_update_product_not_found(client):
    """
    Testa a atualização de um produto que não existe. Deve retornar 404 Not Found.
    """
    response = client.put(
        "/produtos/9999",
        json={"name": "Inexistente", "price": 10.0, "stock": 1}
    )
    assert response.status_code == 404

def test_delete_product(client):
    """
    Testa a deleção de um produto existente. Deve retornar 204 No Content.
    """
    # Cria primeiro
    create_response = client.post(
        "/produtos/",
        json={"name": "Fone de Ouvido", "price": 50.0, "stock": 15}
    )
    product_id = create_response.json()["id"]
    
    # Deleta
    response = client.delete(f"/produtos/{product_id}")
    assert response.status_code == 204
    
    # Verifica que não existe mais
    get_response = client.get(f"/produtos/{product_id}")
    assert get_response.status_code == 404

def test_delete_product_not_found(client):
    """
    Testa a deleção de um produto inexistente. Deve retornar 404 Not Found.
    """
    response = client.delete("/produtos/9999")
    assert response.status_code == 404
