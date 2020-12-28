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

const filter = () => {
    const filters = document.getElementById('filters')
    const selectedState = filters.options[filters.selectedIndex].value
    const url = '/filters'
    fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            state: selectedState
        })
    })
    .then(response => response.json())
    .then(json => renderTasks(json))
}

const renderTasks = (tasksData) => {
    const tasks = document.getElementById("tasks")
    tasks.innerHTML = ''
    console.log(tasksData)
    for (let i = 0; i < tasksData.length; i++) {
        const card = document.createElement('div');
        card.classList.add('card', 'mb-4')
        card.id = 'id_' + tasksData[i].id
        card.style.width = '18rem'

        const cardHeader = document.createElement('h4')
        cardHeader.classList.add('card-header')

        const cardState = document.createElement('input')
        cardState.type = 'checkbox'
        cardState.id = 'check_' + tasksData[i].id
        cardState.setAttribute('onclick', 'setState(' + tasksData[i].id + ')')
        if (tasksData[i].state === 1)
            cardState.setAttribute('checked','checked')

        console.log(tasksData[i].state)
        console.log(cardState.checked)

        cardHeader.appendChild(cardState)
        cardHeader.innerHTML += tasksData[i].title
        card.appendChild(cardHeader)

        const cardBody = document.createElement('div')
        cardBody.classList.add('card-body')

        const taskDesc = document.createElement('p')
        taskDesc.innerText = tasksData[i].description

        const openButton = document.createElement('a')
        openButton.classList.add('btn', 'btn-primary')
        openButton.innerText = 'Открыть'
        openButton.setAttribute('href', '/tasks/' + tasksData[i].id)

        const deleteButton = document.createElement('button')
        deleteButton.innerText = 'Удалить'
        deleteButton.classList.add('btn', 'btn-primary')
        deleteButton.setAttribute('onclick', 'deleteTask(' + tasksData[i].id + ')')

        cardBody.append(taskDesc, openButton, deleteButton)
        card.appendChild(cardBody)

        tasks.appendChild(card)
                    
    //                 // <div class="card-body">
    //                 //     <p>{{ task.description }}</p>
    //                 // <a href="/tasks/{{task.id}}" class="btn btn-primary">Открыть</a>
    //                 // <button class="btn btn-primary" onclick="deleteTask({{task.id}})">Удалить</a>
    //                 // </div>
    // }
    }
}