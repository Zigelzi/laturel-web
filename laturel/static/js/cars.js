
// TODO: Update the car full name value to result cards after clicking the submit button

// Electric vehicle values
const ecarModel = document.getElementById('ecar_model');
const ecarFullModel = document.getElementById('ecar-full-model')
const ecardFullModel = document.getElementById('ecard-full-model')
const ecarPrice = document.getElementById('ecar_price');
const ecarConsumption = document.getElementById('ecar_consumption');
const ecarWeight = document.getElementById('ecar_weight');
const ecarCO2 = document.getElementById('ecar_co2')
const ecarBattery = document.getElementById('ecar-battery')
const ecarOperYearly = document.getElementById('ecar-oper-yearly');
const ecarOperTotal = document.getElementById('ecar-oper-total');
const ecarDeprTotal = document.getElementById('ecar-depr-total');
const ecarCostsTotal = document.getElementById('ecar-costs-total');
const ecarResell = document.getElementById('ecar-resell-value');

var eVars = {
	name: 'eVars'
}

// Gasoline vehicle values
const gcarModel = document.getElementById('gcar_model');
const gcarFullModel = document.getElementById('gcar-full-model')
const gcardFullModel = document.getElementById('gcard-full-model')
const gcarPrice = document.getElementById('gcar_price');
const gcarConsumption = document.getElementById('gcar_consumption');
const gcarCO2 = document.getElementById('gcar_co2')
const gcarOperYearly = document.getElementById('gcar-oper-yearly');
const gcarOperTotal = document.getElementById('gcar-oper-total');
const gcarDeprTotal = document.getElementById('gcar-depr-total');
const gcarCostsTotal = document.getElementById('gcar-costs-total');
const gcarResell = document.getElementById('gcar-resell-value');

var gVars = {
	name: 'gVars'
}

// Diesel vehicle values
const dcarModel = document.getElementById('dcar_model');
const dcarFullModel = document.getElementById('dcar-full-model')
const dcardFullModel = document.getElementById('dcard-full-model')
const dcarPrice = document.getElementById('dcar_price');
const dcarConsumption = document.getElementById('dcar_consumption');
const dcarWeight = document.getElementById('dcar_weight');
const dcarCO2 = document.getElementById('dcar_co2');
const dcarOperYearly = document.getElementById('dcar-oper-yearly');
const dcarOperTotal = document.getElementById('dcar-oper-total');
const dcarDeprTotal = document.getElementById('dcar-depr-total');
const dcarCostsTotal = document.getElementById('dcar-costs-total');
const dcarResell = document.getElementById('dcar-resell-value');

var dVars = {
	name: 'dVars'
}
// General values

const ownTime = document.getElementById('owntime');
const driveKm = document.getElementById('drivekm');
const ownTimeValue = document.querySelectorAll('.owntime')
const jsSubmit = document.getElementById('jsSubmit');
const submitBtn = document.getElementById('submit')
const carInformation = document.getElementById('car-info')
const operationalInformation = document.getElementById('operational-info')
const carHide = document.getElementById('car-hide')

const operationalHide = document.getElementById('operational-hide')

var generalVars = {
	name: 'generalVars',
	owntime: Number(ownTime.value),
	driveKm: Number(driveKm.value)
}


//  Takes car type as input and fetches the data from DB and then updates the information to the input fields.
function updateCarCardData(carType) {

	let model = {
		type: carType.id,
		model: carType.value
	}
	const path = `${window.origin}/db/data`

	// Post selected values to backend to query DB
	fetch(path, {
		method: 'POST',
		credentials: 'include',
		body: JSON.stringify(model),
		cache: 'no-cache',
		headers: new Headers({
			'content-type': 'application/json'
		})
	})
	// Use the response from backend to create JSON object of values
	.then(response => {
		if (response.status !== 200) {
			console.log(`Failed to fetch the data, got response code ${response.status}`);
			return;
		}

		response.json()
				.then(data => {
			// Check which car type the response belongs to and update respecitve values accordingly
			if (carType.id === 'ecar_model'){
				setCarCardTextContents('ecar', data);
			}
			if (carType.id === 'gcar_model'){
				setCarCardTextContents('gcar', data);
			}
			if (carType.id === 'dcar_model'){
				setCarCardTextContents('dcar', data);
			}
		})
	});
}

/**
 * 
 * @param {string} carType The prefix of which type of cars data will be set
 * @param {json} responseData JSON object containing the data of the car received from backend
 */
function setCarCardTextContents(carType, responseData) {
	const fullModel = document.getElementById(`${carType}-full-model`);
	const price = document.getElementById(`${carType}_price`);
	const consumption = document.getElementById(`${carType}_consumption`);
	const co2 = document.getElementById(`${carType}_co2`);

	fullModel.textContent = responseData.car_info.fullmodel;
	price.value = responseData.car_info.price;
	consumption.value = responseData.car_info.consumption;
	co2.value  = Math.floor((responseData.co2.tax * 365) / 100); // Calculating €/year from cnt/day

	if (carType === 'ecar' || carType === 'dcar') {
		const weight = document.getElementById(`${carType}_weight`);
		weight.value = responseData.car_info.weight;
	}
}

/**
 * 
 * @param {HTMLElement} inputElement <input> element from the page
 * @param {*} carType The prefix of which kind of car is being processed
 * @param {*} carObject The car object of this car type
 */
function createCarKeyValuePair(inputElement, carType, carObject) {
	const keyName = inputElement.id.replace(`${carType}_`, '');
	if (isNaN(+inputElement.value)){
		carObject[keyName] = inputElement.value
	}
	else{
		carObject[keyName] = Number(inputElement.value)
	}

}

// Get all vehicle values and append them to their respective objects
function get_car_values(){
	const inputFields = document.querySelectorAll('input');
	for (var i = 0; i < inputFields.length;i++){
		
		// Loop through all the input boxes and respective fields to their values.
		// If value contains number then convert it from str -> int
		if (inputFields[i].id.startsWith('ecar')){
			createCarKeyValuePair(inputFields[i], 'ecar', eVars);
		}
		if (inputFields[i].id.startsWith('gcar')){
			createCarKeyValuePair(inputFields[i], 'gcar', gVars);
		}
		if (inputFields[i].id.startsWith('dcar')){
			createCarKeyValuePair(inputFields[i], 'dcar', dVars);
		}
	}

	var eDeprOper;
	var gDeprOper;
	var dDeprOper;

	// Refresh the general values

	generalVars.owntime = Number(ownTime.value),
	generalVars.driveKm = Number(driveKm.value)

	//Take EV values and calculate the costs
	eVars['carName'] = ecarModel.value;
	eVars['fullModel'] = ecarFullModel.textContent;
	eVars['chargerprice'] = 800;
	eVars['drivingpower'] = calc_drivingpower(eVars.weight, eVars);
	eVars['yearly'] = Math.floor(generalVars.driveKm * eVars.eprice * (eVars.consumption / 100) + eVars.co2 + eVars.drivingpower);
	if (eVars.subsidy > 0 ){
		eVars.price = eVars.price - eVars.subsidy
	}
	eDeprOper = calculateDeprecationAndOperationalCosts(eVars.price, eVars.depr, generalVars.owntime, eVars.yearly);
	eVars = Object.assign(eVars, eDeprOper); // Add the deprecation and operational costs values to main object

	// Take gasoline values and calculate the costs
	gVars['carName'] = gcarModel.value;
	gVars['fullModel'] = gcarFullModel.textContent
	gVars['yearly'] = Math.floor(generalVars.driveKm * gVars.gprice * (gVars.consumption / 100) + gVars.co2);
	gDeprOper = calculateDeprecationAndOperationalCosts(gVars.price, gVars.depr, generalVars.owntime, gVars.yearly);
	gVars = Object.assign(gVars, gDeprOper); // Add the deprecation and operational costs values to main object

	// Take diesel values and calculate costs
	dVars['carName'] = dcarModel.value
	dVars['fullModel'] = dcarFullModel.textContent
	dVars['drivingpower'] = calc_drivingpower(dVars.weight, dVars);
	dVars['yearly'] = Math.floor(generalVars.driveKm * dVars.dprice * (dVars.consumption / 100) + dVars.co2 + dVars.drivingpower);
	dDeprOper = calculateDeprecationAndOperationalCosts(dVars.price, dVars.depr, generalVars.owntime, dVars.yearly);
	dVars = Object.assign(dVars, dDeprOper); // Add the deprecation and operational costs values to main object

	ownTimeValue.forEach(function(ownTimeValue){
		ownTimeValue.textContent = generalVars.owntime;
	})
}

// Update and enter the values to result cards
function update_values(){
	get_car_values()
	
	var lastYear = generalVars.owntime - 1

	ownTimeValue.forEach(function(ownTimeValue){
		ownTimeValue.textContent = generalVars.owntime;
	})
	
	ecarOperYearly.textContent = eVars.yearly;
	ecarOperTotal.textContent = eVars.yearlyCost[lastYear];
	ecarDeprTotal.textContent = eVars.deprValue[lastYear];
	ecarCostsTotal.textContent = (eVars.yearlyCost[lastYear] + eVars.deprValue[lastYear]);
	ecarResell.textContent = (eVars.price - eVars.deprValue[lastYear]);
	ecardFullModel.textContent = ecarFullModel.textContent;

	gcarOperYearly.textContent = gVars.yearly;
	gcarOperTotal.textContent = gVars.yearlyCost[lastYear];
	gcarDeprTotal.textContent = gVars.deprValue[lastYear];
	gcarCostsTotal.textContent = (gVars.yearlyCost[lastYear] + gVars.deprValue[lastYear]);
	gcarResell.textContent = (gVars.price - gVars.deprValue[lastYear]);
	gcardFullModel.textContent = gcarFullModel.textContent;

	dcarOperYearly.textContent = dVars.yearly;
	dcarOperTotal.textContent = dVars.yearlyCost[lastYear];
	dcarDeprTotal.textContent = dVars.deprValue[lastYear];
	dcarCostsTotal.textContent = (dVars.yearlyCost[lastYear] + dVars.deprValue[lastYear]);
	dcarResell.textContent = (dVars.price - dVars.deprValue[lastYear]);
	dcardFullModel.textContent = dcarFullModel.textContent;
	
	

}

function hide_panel(inputElement){

	if (window.getComputedStyle(inputElement).display  === 'none') {
		inputElement.style.display = 'block';
	}
	else {
		inputElement.style.display = 'none';
	}
}

// Helper | Round to last hundred to calculate the driving power tax
function calc_drivingpower(n, obj){
	var drivingpowerTax = 0;
	n = Number(n);
	n = Math.floor(n/100);
	if (obj.name === 'eVars'){
		drivingpowerTax = n * 0.015 * 365 // Finnish driving power tax formula for EV:s
	}
	if (obj.name === 'dVars'){
		drivingpowerTax = n * 0.055 * 365// Finnish driving power tax formula for Diesels
	}
	return Math.floor(drivingpowerTax);
}

// Helper | Calculate deprecation and operational expenses
function calculateDeprecationAndOperationalCosts(purchasePrice, deprecationRate, ownDuration, yearlyCost){
	carValue = [];
	deprValue = [];
	deprYearly = [];
	yearlyCost = [];
	for (var i = 1; i < ownDuration+1; i++){
		carValue.push(purchasePrice * (1 - deprecationRate/100) ** i);
		deprValue.push(Math.floor(purchasePrice - carValue[i -1]))
		if (i === 1){
			deprYearly.push(Math.floor(purchasePrice - carValue[i - 1]))
		}
		else {
			deprYearly.push(Math.floor(carValue[i - 2] - carValue[i - 1]))
		}
	}
	for (var i = 1; i < ownDuration + 1; i++){
		yearlyCost.push(Math.floor(yearlyCost * i))
	}
	return {
		deprValue: deprValue,
		deprYearly: deprYearly,
		yearlyCost:yearlyCost
	}
}

// Eventlisteners for updating the information

document.addEventListener('DOMContentLoaded', () => {updateCarCardData(ecarModel);} );
document.addEventListener('DOMContentLoaded', () => {updateCarCardData(gcarModel);} );
document.addEventListener('DOMContentLoaded', () => {updateCarCardData(dcarModel);} );
document.addEventListener('DOMContentLoaded', update_values);
ecarModel.addEventListener('change', () => {updateCarCardData(ecarModel);} );
gcarModel.addEventListener('change', () => {updateCarCardData(gcarModel);} );
dcarModel.addEventListener('change', () => {updateCarCardData(dcarModel);} );
submitBtn.addEventListener('click', update_values);
carHide.addEventListener('click', () => {hide_panel(carInformation);} );
operationalHide.addEventListener('click', () => {hide_panel(operationalInformation);} );
