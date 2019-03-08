	// const jsonni = document.querySelector('#car_json');
	// var car = {{car_dict|tojson|safe}};

	// jsonni.textContent = car.battery;


	const cars = document.getElementById('car_model');
	cars.addEventListener('change', change_data);	

	function change_data() {

		var model = {
			model: cars.value
		}

		console.log(model)
		var loc = window.origin + '/db/data'

		fetch(loc, {
			method: 'POST',
			credentials: 'include',
			body: JSON.stringify(model),
			cache: 'no-cache',
			headers: new Headers({
				'content-type': 'application/json'
			})
		})
	}