
	const ecars = document.getElementById('ecar_model');
	const gcars = document.getElementById('gcar_model');
	const dcars = document.getElementById('dcar_model');

	const eprice = document.getElementById('ecarprice');
	const econsumption = document.getElementById('econsumption')
	const eweight = document.getElementById('eweight')

	const gprice = document.getElementById('gcarprice');
	const gconsumption = document.getElementById('gconsumption')

	const dprice = document.getElementById('dcarprice');
	const dconsumption = document.getElementById('dconsumption')
	const dweight = document.getElementById('dweight')

	ecars.addEventListener('change', () => {change_data(ecars);});
	gcars.addEventListener('change', () => {change_data(gcars);});
	dcars.addEventListener('change', () => {change_data(dcars);});	

	function change_data(carType) {

		var model = {
			type: carType.id,
			model: carType.value
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
				console.log(data)
				console.log(carType.id)
				if (carType.id === 'ecar_model'){
					eprice.value = data.price;
					eweight.value = data.weight;
					econsumption.value = data.consumption
				}
				if (carType.id === 'gcar_model'){
					gprice.value = data.price;
					gconsumption.value = data.consumption
				}
				if (carType.id === 'dcar_model'){
					dprice.value = data.price;
					dweight.value = data.weight;
					dconsumption.value = data.consumption
				}
			})
		})

		
	}