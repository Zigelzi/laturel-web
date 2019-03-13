
// Electric vehicle values
const ecarModel = document.getElementById('ecar_model');
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
const inputBoxes = document.querySelectorAll('input');
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


//  Updating the  values from car select to respective fields
function change_data(carType) {

	var model = {
		type: carType.id,
		model: carType.value
	}
	
	//console.log(model)  DEBUG
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
			console.log(data)   //DEBUG
			//console.log(carType.id)   DEBUG

			// Check which car type the response belongs to and update respecitve values accordingly
			if (carType.id === 'ecar_model'){
				ecarPrice.value = data.price;
				ecarWeight.value = data.weight;
				ecarConsumption.value = data.consumption
				ecarBattery.value = data.battery
				
			}
			if (carType.id === 'gcar_model'){
				gcarPrice.value = data.price;
				gcarConsumption.value = data.consumption;
				gcarCO2.value = data.co2;
			}
			if (carType.id === 'dcar_model'){
				dcarPrice.value = data.price;
				dcarWeight.value = data.weight;
				dcarConsumption.value = data.consumption;
				dcarCO2.value = data.co2;
			}
		})
	})
}

// Get all vehicle values and append them to their respective objects
function get_car_values(){
	for (var i = 0; i < inputBoxes.length;i++){

		// Loop through all the input boxes and respective fields to their values.
		// If value contains number then convert it from str -> int
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
	var eDeprOper;
	var gDeprOper;
	var dDeprOper;

	// Refresh the general values

	generalVars.owntime = Number(ownTime.value),
	generalVars.driveKm = Number(driveKm.value)

	//Take EV values and calculate the costs
	eVars['carName'] = ecarModel.value;
	eVars['chargerprice'] = 800;
	eVars['drivingpower'] = calc_drivingpower(eVars.weight, eVars);
	eVars['yearly'] = Math.floor(generalVars.driveKm * eVars.eprice * (eVars.consumption / 100) + eVars.tax + eVars.drivingpower);
	if (eVars.subsidy > 0 ){
		eVars.price = eVars.price - eVars.subsidy
	}
	eDeprOper = depr_oper(eVars.price, eVars.depr, generalVars.owntime, eVars.yearly);
	eVars['tax'] = 
	eVars = Object.assign(eVars, eDeprOper); // Add the deprecation and operational costs values to main object

	// Take gasoline values and calculate the costs
	gVars['carName'] = gcarModel.value;
	gVars['yearly'] = Math.floor(generalVars.driveKm * gVars.gprice * (gVars.consumption / 100) + gVars.tax);
	gDeprOper = depr_oper(gVars.price, gVars.depr, generalVars.owntime, gVars.yearly);
	gVars = Object.assign(gVars, gDeprOper); // Add the deprecation and operational costs values to main object

	// Take diesel values and calculate costs
	dVars['carName'] = dcarModel.value
	dVars['drivingpower'] = calc_drivingpower(dVars.weight, dVars);
	dVars['yearly'] = Math.floor(generalVars.driveKm * dVars.dprice * (dVars.consumption / 100) + dVars.tax + dVars.drivingpower);
	dDeprOper = depr_oper(dVars.price, dVars.depr, generalVars.owntime, dVars.yearly);
	dVars = Object.assign(dVars, dDeprOper); // Add the deprecation and operational costs values to main object

	ownTimeValue.forEach(function(ownTimeValue){
		ownTimeValue.textContent = generalVars.owntime;
	})
}

// Update and enter the values to result cards
function update_values(e){
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

	gcarOperYearly.textContent = gVars.yearly;
	gcarOperTotal.textContent = gVars.yearlyCost[lastYear];
	gcarDeprTotal.textContent = gVars.deprValue[lastYear];
	gcarCostsTotal.textContent = (gVars.yearlyCost[lastYear] + gVars.deprValue[lastYear]);
	gcarResell.textContent = (gVars.price - gVars.deprValue[lastYear]);

	dcarOperYearly.textContent = dVars.yearly;
	dcarOperTotal.textContent = dVars.yearlyCost[lastYear];
	dcarDeprTotal.textContent = dVars.deprValue[lastYear];
	dcarCostsTotal.textContent = (dVars.yearlyCost[lastYear] + dVars.deprValue[lastYear]);
	dcarResell.textContent = (dVars.price - dVars.deprValue[lastYear]);


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
function depr_oper(purchase, rate, years, cost){
	carValue = [];
	deprValue = [];
	deprYearly = [];
	yearlyCost = [];
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
	return {
		deprValue: deprValue,
		deprYearly: deprYearly,
		yearlyCost:yearlyCost
	}
}



// Eventlisteners for updating the information
document.addEventListener('DOMContentLoaded', update_values);
ecarModel.addEventListener('change', () => {change_data(ecarModel);} );
gcarModel.addEventListener('change', () => {change_data(gcarModel);} );
dcarModel.addEventListener('change', () => {change_data(dcarModel);} );
submitBtn.addEventListener('click', update_values);
carHide.addEventListener('click', () => {hide_panel(carInformation);} );
operationalHide.addEventListener('click', () => {hide_panel(operationalInformation);} );
