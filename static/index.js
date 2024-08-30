// scripts.js

const BASEURL = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('cadastro-form');
    const produtoIdInput = document.getElementById('id-produto');
    const produtosTable = document.getElementById('tabela-produtos').getElementsByTagName('tbody')[0];

    function fetchProdutos() {
        fetch(`${BASEURL}/`)
            .then(response => response.json())
            .then(data => {
                produtosTable.innerHTML = '';
                data.forEach(produto => {
                    const row = produtosTable.insertRow();
                    row.insertCell().innerText = produto.id;
                    row.insertCell().innerText = produto.nome;
                    row.insertCell().innerText = produto.codigo;
                    row.insertCell().innerText = produto.descricao;
                    row.insertCell().innerText = produto.preco.toFixed(2);
                    const actionsCell = row.insertCell();
                    actionsCell.innerHTML = `
                        <button class="action" onclick="editProduto(${produto.id})">Editar</button>
                        <button class="action" onclick="deleteProduto(${produto.id})">Excluir</button>
                    `;
                });
            });
    }

    window.editProduto = function(id) {
        fetch(`${BASEURL}/${id}`)
            .then(response => response.json())
            .then(produto => {
                produtoIdInput.value = produto.id;
                document.getElementById('nome').value = produto.nome;
                document.getElementById('codigo').value = produto.codigo;
                document.getElementById('descricao').value = produto.descricao || '';
                document.getElementById('preco').value = produto.preco;
            });
    }

    window.deleteProduto = function(id) {
        fetch(`${BASEURL}/${id}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(() => {
                fetchProdutos();
            });
    }

    form.addEventListener('submit', event => {
        event.preventDefault();

        const id = produtoIdInput.value;
        const method = id ? 'PUT' : 'POST';
        const url = id ? `${BASEURL}/${id}` : `${BASEURL}`;

        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                nome: document.getElementById('nome').value,
                codigo: document.getElementById('codigo').value,
                descricao: document.getElementById('descricao').value,
                preco: parseFloat(document.getElementById('preco').value),
            }),
        })
            .then(response => response.json())
            .then(() => {
                form.reset();
                produtoIdInput.value = '';
                fetchProdutos();
            });
    });

    fetchProdutos();
});
