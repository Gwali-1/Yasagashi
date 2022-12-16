"use strict"



const  locationSelect = document.querySelector(".select-filter");
const priceForm = document.querySelector(".price-form");
const minPrice= document.querySelector(".min-price");
const maxPrice= document.querySelector(".max-price");
const priceFormSubmitBtn = document.querySelector(".price-btn");

const saleRadioBtn = document.querySelector(".sale-radio");
const rentRadioBtn = document.querySelector(".rent-radio");
const token = document.querySelector("meta[name='token']").getAttribute("content");









priceForm.onsubmit = function (e){
    e.preventDefault();
    const form = new FormData(priceForm);
    const min = Number(form.get("minimum-price"));
    const max = Number(form.get("maximum-price"));



    if (Number.isNaN(min) || Number.isNaN(max)){
        console.log("enter valid numbers");
        console.log(`min=${min},max=${max}`);
        return

    }

    if(max < min){
        console.log("no");
        return;
    }

    fetch("/home/page/1",{
        method:"POST",
        headers:{"X-CSRFToken":token},
        body:JSON.stringify({
            action:"price_filter",
            min_price:min,
            max_price:max
        })
    }).then(response => response.json()).then( result => {

        ///////////TODO
        console.log(result);
    })
    .catch(error => console.log(error))

    
}






locationSelect.onchange = function(e){
    fetch("/home/page/1",{
        method:"POST",
        headers:{"X-CSRFToken":token},
        body:JSON.stringify({
            action:"location_filter",
            location:this.value
        })
    }).then(response => response.json()).then(result =>{

        //////////////TODO
        console.log(result);
    }).catch(error => console.log(error))
}






saleRadioBtn.onchange = function(e){
    if(this.checked = true){
        if(rentRadioBtn.checked = true) rentRadioBtn.checked = false;

        fetch("/home/page/1",{
            method:"POST",
            headers:{"X-CSRFToken":token},
            body:JSON.stringify({
                action:"sale_filter",
            })
        }).then(response => response.json()).then(result => {

            ///TODO
            console.log(result);
        }).catch(error => console.log(error))

    }else{
        console.log("ss")
    }


    
}





rentRadioBtn.onchange = function(e){
    if(this.checked = true){
        if(saleRadioBtn.checked = true) saleRadioBtn.checked = false;

        fetch("/home/page/1",{
            method:"POST",
            headers:{"X-CSRFToken":token},
            body:JSON.stringify({
                action:"rent_filter",
            })
        }).then(response => response.json()).then(result => {

            ////TODO
            console.log(result);
        }).catch(error => console.log(error))

    }else{
        console.log("ss")
    }


    
}