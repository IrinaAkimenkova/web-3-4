const deleteTask = (id) => {
    const url = '/tasks/' + id;

    fetch(url, {
        method: 'DELETE'
    })
    .then(() => {
        const card = document.querySelector('.card#id_' + id);
        card.remove();
    })
    .catch((e) => {
        alert(e.message)
    })
}

const setState = (id) => {
    const url = '/tasks/' + id;

    fetch(url, {
        method: 'PUT'
    })
    .catch((e) => {
        alert(e.message)
    })
}

const getComment = (id) => {
    const url = `https://jsonplaceholder.typicode.com/comments?postId=${id}`;

    fetch(url)
        .then(response => response.json())
        .then(json => {
            const comments = document.getElementById('this_card');
            const comment = document.createElement('p');
            comment.innerText = json[0]['body'];
            comments.appendChild(comment);
        })
}

const changeTask = (id) => {
    const url = '/tasks/desc/' + id;
    const newDesc = document.getElementById("newDesc")
    console.log(newDesc.value)
    fetch(url, {
        method: 'PUT',
        body: newDesc.value
    })
}