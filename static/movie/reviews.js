function display(movie_id) {
	let xhr = new XMLHttpRequest();

	xhr.open('GET', `/movie/getreviews/${movie_id}`, true);
	xhr.onreadystatechange = () => {
		if(xhr.readyState == 4 && xhr.status == 200) {
			let reviews = JSON.parse(xhr.responseText);
			for(let i = 0; i < reviews.length; i++) {
				let review = reviews[i];
				let review_container = document.createElement('div');
				review_container.classList.add('review');
				

				let review_title = document.createElement('h1');
				review_title.textContent = review['review_title'];

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

				review_container.appendChild(review_title);
				review_container.appendChild(author_stars);
				review_container.appendChild(review_content);
				document.getElementById(`reviews_container${i%3}`).appendChild(review_container);
			}
		}
	}
	xhr.send();
}
