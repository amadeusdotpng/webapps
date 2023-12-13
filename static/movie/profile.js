function display() {
	let xhr = new XMLHttpRequest();

	xhr.open('GET', '/movie/getreviewsself', true);
	xhr.onreadystatechange = () => {
		if(xhr.readyState == 4 && xhr.status == 200) {
			let reviews = JSON.parse(xhr.responseText);
			let profile_reviews = document.getElementById('profile_reviews');
			profile_reviews.innerHTML = '';
			for(let i = 0; i < reviews.length; i++) {
				let review = reviews[i];
				let review_id = review['id']
				let review_container = document.createElement('div');
				review_container.classList.add('review');
				
				
				let review_wrapper = document.createElement('div')
				review_wrapper.classList.add('review_wrapper')
				let review_title = document.createElement('h1');
				review_title.textContent = review['review_title'];

				let trashcan = document.createElement('img');
				trashcan.src = '/static/todo/assets/trashcan.png';
				trashcan.alt = 'trashcan';
				trashcan.width = '24';
				trashcan.height = '24';
				trashcan.onclick = function() {del_review(review_id)};

				review_wrapper.appendChild(review_title);
				review_wrapper.appendChild(trashcan);

				let author_stars = document.createElement('div');
				author_stars.classList.add('author_stars')

				let author = document.createElement('h2');
				author.textContent = review['author'] + ' - ';
				author_stars.appendChild(author);

				for(let j = 0; j < review['movie_rating']; j++) {
					let star = document.createElement('span');
					star.classList.add('fa');
					star.classList.add('fa-star');
					star.classList.add('star-checked');
					author_stars.appendChild(star)
				}

				for(let j = 0; j < 5-review['movie_rating']; j++) {
					let star = document.createElement('span');
					star.classList.add('fa');
					star.classList.add('fa-star');
					author_stars.appendChild(star)
				}


				let review_content = document.createElement('p');
				review_content.textContent = review['review_content'];

				review_container.appendChild(review_wrapper);
				review_container.appendChild(author_stars);
				review_container.appendChild(review_content);
				profile_reviews.appendChild(review_container);
			}
		}
	}
	xhr.send();
}

window.onload = display();

function del_review(review_id) {
	console.log('hey')
	const url = `/movie/del-post/${review_id}`

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
