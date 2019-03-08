
	const ecars = document.getElementById('car_model');
	const eprice = document.getElementById('ecarprice');
	const econsumption = document.getElementById('econsumption')
	const eweight = document.getElementById('eweight')
	ecars.addEventListener('change', change_data);	

	function change_data() {

		var model = {
			model: ecars.value
		}

		console.log(model)
		var loc = `${window.origin}/db/data`

		fetch(loc, {
			method: 'POST',
			credentials: 'include',
			body: JSON.stringify(model),
			cache: 'no-cache',
			headers: new Headers({
				'content-type': 'application/json'
			})
		})
		.then(function(response) {
			if (response.status !== 200) {
				console.log(`Response status not 200: ${response.status}`);
				return;
			}

			response.json().then(function(data){
				eprice.value = data.price;
				eweight.value = data.weight;
				econsumption.value = data.consumption


			})
		})

		
	}