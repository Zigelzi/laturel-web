// TODO: Update the car full name value to result cards after clicking the submit button

const ecarModel = document.getElementById('ecar_model');
const gcarModel = document.getElementById('gcar_model');
const dcarModel = document.getElementById('dcar_model');

const ownTime = document.getElementById('owntime');
const driveKm = document.getElementById('drivekm');
const submitBtn = document.getElementById('submit')

let eVars = {
	name: 'eVars'
}
let gVars = {
	name: 'gVars'
}
let dVars = {
	name: 'dVars'
}
let generalVars = {
	name: 'generalVars',
}

function update_values(){
	get_car_values();
	updateOwnTimeTextContents();
	
	updateCarResultCard('ecar', eVars);
	updateCarResultCard('gcar', gVars);
	updateCarResultCard('dcar', dVars);
	
}

// Get all vehicle values and append them to their respective objects
function get_car_values(){
	readUserInputsForAllCarTypes()

	// Refresh the general values
	updateOwntime();
	updateDriveAmount();

	//Take EV values and calculate the costs
	addModelInformationFor(eVars);
	updateCostsToCarObject('ecar', eVars)
	
	// Take gasoline values and calculate the costs
	addModelInformationFor(gVars);
	updateCostsToCarObject('gcar', gVars)

	// Take diesel values and calculate costs
	addModelInformationFor(dVars);
	updateCostsToCarObject('dcar', dVars)

}

function readUserInputsForAllCarTypes() {
	const inputFields = document.querySelectorAll('input');
	for (let i = 0; i < inputFields.length;i++){
		
		// Loop through all the input boxes and respective fields to their values.
		// If value contains number then convert it from str -> int
		if (inputFields[i].id.startsWith('ecar')){
			createKeyValuePairFromInput(inputFields[i], 'ecar', eVars);
		}
		if (inputFields[i].id.startsWith('gcar')){
			createKeyValuePairFromInput(inputFields[i], 'gcar', gVars);
		}
		if (inputFields[i].id.startsWith('dcar')){
			createKeyValuePairFromInput(inputFields[i], 'dcar', dVars);
		}
	}
}

function updateOwnTimeTextContents() {
	const ownTimeValue = document.querySelectorAll('.owntime');

	ownTimeValue.forEach(function(ownTimeValue){
		ownTimeValue.textContent = generalVars.ownTime;
	})
}

function updateCarResultCard(carType, carObject) {
	const operationalYearlyCost = document.getElementById(`${carType}-oper-yearly`)
	const totalOperationalCost = document.getElementById(`${carType}-oper-total`);
	const totalDeprecationCost = document.getElementById(`${carType}-depr-total`);
	const totalCostOfOwnership = document.getElementById(`${carType}-costs-total`);
	const carResellPrice = document.getElementById(`${carType}-resell-value`);
	const resultCardCarFullModel = document.getElementById(`${carType}-resultcard-full-model`);

	let lastYear = generalVars.ownTime - 1 // Requires -1 because zero indexed arrays

	operationalYearlyCost.textContent = carObject.yearlyOperationalCost;
	totalOperationalCost.textContent = carObject.totalOperationalCostPerYear[lastYear];
	totalDeprecationCost.textContent = carObject.totalDeprecationCostPerYear[lastYear];
	totalCostOfOwnership.textContent = (carObject.totalOperationalCostPerYear[lastYear] + carObject.totalDeprecationCostPerYear[lastYear]);
	carResellPrice.textContent = (carObject.price - carObject.totalDeprecationCostPerYear[lastYear]);
	resultCardCarFullModel.textContent = carObject.fullModel;
}

/**
 * 
 * @param {HTMLElement} inputElement <input> element from the page
 * @param {*} carType The prefix of which kind of car is being processed
 * @param {*} carObject The car object of this car type
 */
function createKeyValuePairFromInput(inputElement, carType, carObject) {
	const keyName = inputElement.id.replace(`${carType}_`, '');
	if (isNaN(+inputElement.value)){
		carObject[keyName] = inputElement.value
	}
	else{
		carObject[keyName] = Number(inputElement.value)
	}

}

function updateOwntime() {
	const ownTime = document.getElementById('owntime');
	generalVars.ownTime = Number(ownTime.value)
}

function updateDriveAmount() {
	const driveKm = document.getElementById('drivekm');
	generalVars.driveKm = Number(driveKm.value)
}

function addModelInformationFor(carObject) {
	let carType = '';

	if (carObject.name === 'eVars') {
		carType = 'ecar'
	}
	if (carObject.name === 'gVars') {
		carType = 'gcar'
	}
	if (carObject.name === 'dVars') {
		carType = 'dcar'
	}

	let carModel = document.getElementById(`${carType}_model`);
	let fullCarModel = document.getElementById(`${carType}-full-model`);

	carObject['model'] = carModel.value;
	carObject['fullModel'] = fullCarModel.textContent;	
}

function updateCostsToCarObject(carType, carObject) {
	if (carObject.name === 'eVars') {
		carObject['chargerprice'] = 800;
	}
	if (carObject.name === 'eVars' || carObject.name === 'dVars') {
		carObject['drivingpower'] = calculateCarDrivingTax(carObject.weight, carObject);
	}
	
	carObject['yearlyOperationalCost'] = calculateYearlyOperationalCosts(carType);
	carObject['totalDeprecationCostPerYear'] = calculateTotalDeprecationCostPerYear(generalVars.ownTime, carObject.price, carObject.depr);
	carObject['totalOperationalCostPerYear'] = calculateTotalOperationalCostPerYear(generalVars.ownTime, carObject.yearlyOperationalCost);
	carObject.price = calculateEcarSubsidisedPrice();
}

// Driving power tax is only applicable for electric vehicles and diesel passanger vehicles in Finland
// See details from Traficom website: https://www.traficom.fi/en/transport/road/structure-and-quantity-vehicle-tax
function calculateCarDrivingTax(carWeight, carObject){
	let drivingpowerTax = 0;
	let evTax = 0.015 //  Eurocents. Tax per every starting 100 kg:s of vehicles total mass
	let dieselTax = 0.055 //  Eurocents. Tax per every starting 100 kg:s of vehicles total mass
	const daysInYear = 365;

	carWeight = Number(carWeight);
	carWeight = Math.floor(carWeight/100); // Dividing by 100 because the law states for every 100 starting kilos.

	if (carObject.name === 'eVars'){
		drivingpowerTax = carWeight * evTax * daysInYear // Finnish driving power tax formula for EV:s
	}
	if (carObject.name === 'dVars'){
		drivingpowerTax = carWeight * dieselTax * daysInYear // Finnish driving power tax formula for Diesels
	}
	drivingpowerTax = Math.floor(drivingpowerTax)

	return drivingpowerTax;
}

function calculateYearlyOperationalCosts(carType){
	let yearlyOperationalCost = 0;
	if (carType === 'ecar'){
		yearlyOperationalCost= Math.floor(generalVars.driveKm * eVars.eprice * (eVars.consumption / 100) + eVars.co2 + eVars.drivingpower);
	}
	if (carType === 'gcar') {
		yearlyOperationalCost = Math.floor(generalVars.driveKm * gVars.gprice * (gVars.consumption / 100) + gVars.co2);
	}
	if (carType === 'dcar') {
		yearlyOperationalCost = Math.floor(generalVars.driveKm * dVars.dprice * (dVars.consumption / 100) + dVars.co2 + dVars.drivingpower);
	}
	return yearlyOperationalCost;
}

function calculateEcarSubsidisedPrice() {
	let subsidiedPrice = eVars.price;

	if ( eVars.subsidy > 0 ){
		subsidiedPrice = eVars.price - eVars.subsidy
	}

	return subsidiedPrice;
}

function calculateTotalDeprecationCostPerYear(ownTime, carPurchasePrice, deprecationRate) {
	let carYearlyValues = []
	let deprecationCostPerYear = []
	for (let currentYear = 1; currentYear <= ownTime; currentYear++){
		carYearlyValues.push(carPurchasePrice * (1 - deprecationRate/100) ** currentYear);
		deprecationCostPerYear.push(Math.floor(carPurchasePrice - carYearlyValues[currentYear -1]))
	}
	return deprecationCostPerYear;
}

function calculateTotalOperationalCostPerYear(ownTime, oneYearOperationalCost) {
	let operationalCostPerYear = []
	for (let currentYear = 1; currentYear <= ownTime; currentYear++){
		operationalCostPerYear.push(Math.floor(oneYearOperationalCost * currentYear))
	}
	return operationalCostPerYear;

}

//  Takes car type as input and fetches the data from DB and then updates the information to the input fields.
function retrieveCarDataAndUpdateCarCards(carType) {

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
				setCarOperationalCostsCardInputContents('ecar', data);
			}
			if (carType.id === 'gcar_model'){
				setCarOperationalCostsCardInputContents('gcar', data);
			}
			if (carType.id === 'dcar_model'){
				setCarOperationalCostsCardInputContents('dcar', data);
			}
		})
	});
}

/**
 * 
 * @param {string} carType The prefix of which type of cars data will be set
 * @param {json} responseData JSON object containing the data of the car received from backend
 */
function setCarOperationalCostsCardInputContents(carType, responseData) {
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

// Eventlisteners for updating the information

document.addEventListener('DOMContentLoaded', () => {retrieveCarDataAndUpdateCarCards(ecarModel);} );
document.addEventListener('DOMContentLoaded', () => {retrieveCarDataAndUpdateCarCards(gcarModel);} );
document.addEventListener('DOMContentLoaded', () => {retrieveCarDataAndUpdateCarCards(dcarModel);} );
document.addEventListener('DOMContentLoaded', update_values);

ecarModel.addEventListener('change', () => {retrieveCarDataAndUpdateCarCards(ecarModel);} );
gcarModel.addEventListener('change', () => {retrieveCarDataAndUpdateCarCards(gcarModel);} );
dcarModel.addEventListener('change', () => {retrieveCarDataAndUpdateCarCards(dcarModel);} );

submitBtn.addEventListener('click', update_values);
