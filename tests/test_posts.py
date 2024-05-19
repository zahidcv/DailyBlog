def test_get_all_posts(authorized_client):
    res = authorized_client.get("/blog/all")
    print(res.json())
    assert res.status_code == 200
    
    
    