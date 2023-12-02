function display() {
	let xhr = new XMLHttpRequest();

	xhr.open('GET', '/todo-login/list', true);
	xhr.onreadystatechange = () => {
		if(xhr.readyState == 4 && xhr.status == 200) {
			let lists = JSON.parse(xhr.responseText);
			let list_container = document.getElementById('lists')
			list_container.innerHTML = "";
			for(let i = 0; i < lists.length; i++) {
				let list_data = lists[i];
				let items = document.createElement('ul');

				for(let j = 0; j < list_data.items.length; j++) {
					let item_data = list_data.items[j];

					let item_trashcan = document.createElement('img');
					item_trashcan.src = '/static/todo/assets/trashcan.png';
					item_trashcan.alt = 'trashcan';
					item_trashcan.width = '16';
					item_trashcan.height = '16';
					item_trashcan.onclick = function() {del_item(list_data.listid, item_data.itemid)};

					let item = document.createElement('li');
					item.textContent = item_data.name;
					item.onclick = function() {toggle(list_data.listid, item_data.itemid)};
					item.appendChild(item_trashcan);

					if(item_data.is_complete) {
						item.classList.add('completed');
						item.classList.remove('incomplete');
					} else {
						item.classList.add('incomplete');
						item.classList.remove('completed');
					}

					items.appendChild(item);
				}

				let list_trashcan = document.createElement('img');
				list_trashcan.src = '/static/todo/assets/trashcan.png';
				list_trashcan.alt = 'trashcan';
				list_trashcan.width = '24';
				list_trashcan.height = '24';
				list_trashcan.onclick = function() {del_list(list_data.listid)};

				let list_title = document.createElement('h1');
				list_title.textContent = list_data.name;
				list_title.classList.add('list-title')
				list_title.appendChild(list_trashcan);
				
				let list_content = document.createElement('div');
				list_content.classList.add('list-content');
				list_content.appendChild(items);

				let add_text = document.createElement('input');
				add_text.type = 'text';
				add_text.placeholder = 'Your new task\'s name';
				add_text.id = `item_name${list_data.listid}`;
				add_text.classList.add('item-name')

				let add_btn = document.createElement('input');
				add_btn.type = 'button';
				add_btn.value = 'Add Task';
				add_btn.onclick = function() {add_item(list_data.listid)};

				let add_div = document.createElement('div');
				add_div.classList.add('add-item');
				add_div.appendChild(add_text);
				add_div.appendChild(add_btn);

				let list_div = document.createElement('div');
				list_div.classList.add('list');
				list_div.appendChild(list_title);
				list_div.appendChild(list_content);
				list_div.appendChild(add_div);


				list_container.appendChild(list_div);
			}
		}
	};
	xhr.send();
}

window.onload = display();

function toggle(list_id, item_id) {
	const url = `/todo-login/toggleitem/${list_id}/${item_id}`;

	fetch(url, {
		method: 'GET',
	})
	.then(response => {
		if(!response.ok) {
			return Promise.reject('Failed to toggle item');
		}
		display();
		return;
	});
}

function add_list() {
	let elem = document.getElementById('list_name');
	let name = elem.value;
	if(!name) {
		return;
	}
	const url = `/todo-login/addlist?name=${encodeURIComponent(name)}`;

	fetch(url, {
		method: 'GET',
	}).then(response => {
		if(!response.ok) {
			return Promse.reject('Failed to add list');
		}
		display();
	})

	elem.value = "";

}

function add_item(list_id) {
	let elem = document.getElementById(`item_name${list_id}`)
	let name = elem.value;
	if(!name) {
		return;
	}
	const url = `/todo-login/additem/${list_id}?name=${name}`

	fetch(url, {
		method: 'GET',
	})
	.then(response => {
		if(!response.ok) {
			return Promise.reject('Failed to add to list');
		}
		display();
	});
	elem.value = "";
}

function del_item(list_id, item_id) {
	const url = `/todo-login/delitem/${list_id}/${item_id}`

	fetch(url, {
		method: 'GET',
	})
	.then(response => {
		if(!response.ok) {
			return Promise.reject('Failed to delete from list');
		}
		display();
	});
}

function del_list(list_id) {
	const url = `/todo-login/dellist/${list_id}`

	fetch(url, {
		method: 'GET',
	})
	.then(response => {
		if(!response.ok) {
			return Promise.reject('Failed to delete list');
		}
		display();
	});
}
