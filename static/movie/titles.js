function display() {
	let xhr = new XMLHttpRequest();

	xhr.open('GET', '/movie/gettitles', true);
	xhr.onreadystatechange = () => {
		if(xhr.readyState == 4 && xhr.status == 200) {
			let titles = JSON.parse(xhr.responseText);
			let titles_container = document.getElementById('titles_container');

			for(let id in titles) {
				let title = titles[id]
				let title_container = document.createElement('div');
				title_container.classList.add('title');
				
				let review_link = document.createElement('a');
				review_link.href = '/movie/reviews/'+id;

				let movie_title = document.createElement('h1');
				movie_title.textContent = title['movie_title'];
				review_link.appendChild(movie_title);

				let rating = document.createElement('div');
				rating.classList.add('star_rating');

				let avg = Math.round(10 * title['total_rating']/title['review_count']) / 10
				let average_rating = document.createElement('h2');
				average_rating.textContent = avg+ ' - ';
				rating.appendChild(average_rating)

				for(let j = 0; j < Math.floor(avg); j++) {
					let star = document.createElement('span');
					star.classList.add('fa');
					star.classList.add('fa-star');
					star.classList.add('star-checked');
					rating.appendChild(star)
				}

				for(let j = 0; j < Math.ceil(5-avg); j++) {
					let star = document.createElement('span');
					star.classList.add('fa');
					star.classList.add('fa-star');
					rating.appendChild(star)
				}

				
				let review_count = document.createElement('h3');
				review_count.textContent = 'Total Reviews: ' + title['review_count'];

				title_container.appendChild(review_link);
				title_container.appendChild(rating);
				title_container.appendChild(review_count);

				titles_container.appendChild(title_container);
			}
		}
	};
	xhr.send();
}

window.onload = display();
