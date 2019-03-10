
// Electric vehicle values
const ecars = document.getElementById('ecar_model');
const ecarprice = document.getElementById('ecarprice');
const econsumption = document.getElementById('econsumption')
const eweight = document.getElementById('eweight')
var evars = {}

// Gasoline vehicle values
const gcars = document.getElementById('gcar_model');
const gcarprice = document.getElementById('gcarprice');
const gconsumption = document.getElementById('gconsumption')
var gvars = {}

// Diesel vehicle values
const dcars = document.getElementById('dcar_model');
const dcarprice = document.getElementById('dcarprice');
const dconsumption = document.getElementById('dconsumption')
const dweight = document.getElementById('dweight')
var dvars = {}

// General values
const inputBoxes = document.querySelectorAll('input')

// Update car values from car select menu
ecars.addEventListener('change', () => {change_data(ecars);} );
gcars.addEventListener('change', () => {change_data(gcars);} );
dcars.addEventListener('change', () => {change_data(dcars);} );	

//  Updating the  values from car select to respective fields
function change_data(carType) {

	var model = {
		type: carType.id,
		model: carType.value
	}
	
	console.log(model) // DEBUG
	var loc = `${window.origin}/db/data`

	// Post selected values to backend to query DB
	fetch(loc, {
		method: 'POST',
		credentials: 'include',
		body: JSON.stringify(model),
		cache: 'no-cache',
		headers: new Headers({
			'content-type': 'application/json'
		})
	})
	// Use the response from backend to create JSON object of values
	.then(function(response) {
		if (response.status !== 200) {
			console.log(`Response status not 200: ${response.status}`);
			return;
		}

		response.json().then(function(data){
			console.log(data)  // DEBUG
			console.log(carType.id)  // DEBUG

			// Check which car type the response belongs to and update respecitve values accordingly
			if (carType.id === 'ecar_model'){
				ecarprice.value = data.price;
				eweight.value = data.weight;
				econsumption.value = data.consumption
			}
			if (carType.id === 'gcar_model'){
				gcarprice.value = data.price;
				gconsumption.value = data.consumption
			}
			if (carType.id === 'dcar_model'){
				dcarprice.value = data.price;
				dweight.value = data.weight;
				dconsumption.value = data.consumption
			}
		})
	})
}


function get_car_values(){
	for (var i = 0; i < inputBoxes.length;i++){
		if (inputBoxes[i].id.startsWith('e')){
		  evars[inputBoxes[i].id] = inputBoxes[i].value
		}
		if (inputBoxes[i].id.startsWith('g')){
			gvars[inputBoxes[i].id] = inputBoxes[i].value
		  }
		  if (inputBoxes[i].id.startsWith('d')){
			dvars[inputBoxes[i].id] = inputBoxes[i].value
		  }
	  }
}