import pytest
from business_object.admin import Admin  
def test_initialisation():
    admin = Admin("Alice", "secure123")
    assert admin.nom == "Alice"
    assert admin.mdp == "secure123"


