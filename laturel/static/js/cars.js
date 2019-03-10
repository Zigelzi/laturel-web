
// Electric vehicle values
const ecars = document.getElementById('ecar_model');
const ecar_price = document.getElementById('ecar_price');
const ecar_consumption = document.getElementById('ecar_consumption');
const ecar_weight = document.getElementById('ecar_weight');
const ecar_depr = document.getElementById('ecar_depr');

var eVars = {
	name: 'eVars'
}

// Gasoline vehicle values
const gcars = document.getElementById('gcar_model');
const gcar_price = document.getElementById('gcar_price');
const gcar_consumption = document.getElementById('gcar_consumption');
const gcar_depr = document.getElementById('gcar_depr');
var gVars = {
	name: 'gVars'
}

// Diesel vehicle values
const dcars = document.getElementById('dcar_model');
const dcar_price = document.getElementById('dcar_price');
const dcar_consumption = document.getElementById('dcar_consumption')
const dcar_weight = document.getElementById('dcar_weight')
const dcar_depr = document.getElementById('dcar_depr');
var dVars = {
	name: 'dVars'
}
// General values
const inputBoxes = document.querySelectorAll('input');
const ownTime = document.getElementById('owntime');
const driveKm = document.getElementById('drivekm');
var generalVars = {
	name: 'generalVars',
	owntime: Number(ownTime.value),
	driveKm: Number(driveKm.value)
}


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
				ecar_price.value = data.price;
				ecar_weight.value = data.weight;
				ecar_consumption.value = data.consumption
			}
			if (carType.id === 'gcar_model'){
				gcar_price.value = data.price;
				gcar_consumption.value = data.consumption
			}
			if (carType.id === 'dcar_model'){
				dcar_price.value = data.price;
				dcar_weight.value = data.weight;
				dcar_consumption.value = data.consumption
			}
		})
	})
}

// Get all vehicle values and append them to their respective objects
function get_car_values(){
	for (var i = 0; i < inputBoxes.length;i++){
		if (inputBoxes[i].id.startsWith('ecar')){
			if (isNaN(+inputBoxes[i].value)){
				eVars[inputBoxes[i].id.replace('ecar_','')] = inputBoxes[i].value
			}
			else{
				eVars[inputBoxes[i].id.replace('ecar_','')] = Number(inputBoxes[i].value)
			}
		}
		if (inputBoxes[i].id.startsWith('gcar')){
			if (isNaN(+inputBoxes[i].value)){
				gVars[inputBoxes[i].id.replace('gcar_','')] = inputBoxes[i].value
			}
			else{
				gVars[inputBoxes[i].id.replace('gcar_','')] = Number(inputBoxes[i].value)
			}
		}
		if (inputBoxes[i].id.startsWith('dcar')){
			if (isNaN(+inputBoxes[i].value)){
				dVars[inputBoxes[i].id.replace('dcar_','')] = inputBoxes[i].value
			}
			else{
				dVars[inputBoxes[i].id.replace('dcar_','')] = Number(inputBoxes[i].value)
			}
		}
	}
	eVars['chargerprice'] = 800
	eVars['drivingpower'] = calc_drivingpower(eVars.weight, eVars)
	eVars['yearly'] = Math.floor(generalVars.driveKm * eVars.eprice * (eVars.consumption / 100) + eVars.tax + eVars.drivingpower)
	if (eVars.subsidy > 0 ){
		eVars.price = eVars.price - eVars.subsidy
	}
	 
	
	gVars['yearly'] = Math.floor(generalVars.driveKm * gVars.gprice * (gVars.consumption / 100) + gVars.tax)

	dVars['drivingpower'] = calc_drivingpower(dVars.weight, dVars)
	dVars['yearly'] = Math.floor(generalVars.driveKm * dVars.dprice * (dVars.consumption / 100) + dVars.tax + dVars.drivingpower)	  
}

// Helper | Round to last hundred to calculate the driving power tax
function calc_drivingpower(n, obj){
	var drivingpowerTax = 0
	n = Number(n)
	n = Math.floor(n/100)
	if (obj.name === 'eVars'){
		drivingpowerTax = n * 0.015 * 365 // Finnish driving power tax formula for EV:s
	}
	if (obj.name === 'dVars'){
		drivingpowerTax = n * 0.055 * 365// Finnish driving power tax formula for Diesels
	}
	return drivingpowerTax
}

// Helper | Calculate deprecation and operational expenses
function depr_oper(purchase, rate, years, cost){
	carValue = []
	deprValue = []
	deprYearly = []
	yearlyCost = []
	for (var i = 1; i < years+1; i++){
		carValue.push(purchase * (1 - rate/100) ** i);
		deprValue.push(Math.floor(purchase - carValue[i -1]))
		if (i === 1){
			deprYearly.push(Math.floor(purchase - carValue[i - 1]))
		}
		else {
			deprYearly.push(Math.floor(carValue[i - 2] - carValue[i - 1]))
		}
	}
	for (var i = 1; i < years + 1; i++){
		yearlyCost.push(Math.floor(cost * i))
	}
	console.log(deprValue)
	console.log(deprYearly)
	console.log(yearlyCost)
	return {
		deprValue: deprValue,
		deprYearly: deprYearly,
		yearlyCost:yearlyCost
	}
}



// Update car values from car select menu
ecars.addEventListener('change', () => {change_data(ecars);} );
gcars.addEventListener('change', () => {change_data(gcars);} );
dcars.addEventListener('change', () => {change_data(dcars);} );
document.addEventListener('DOMContentLoaded', get_car_values);	
