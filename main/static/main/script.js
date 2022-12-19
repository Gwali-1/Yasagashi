"use strict"



const  locationSelect = document.querySelector(".select-filter");
const priceForm = document.querySelector(".price-form");
const minPrice= document.querySelector(".min-price");
const maxPrice= document.querySelector(".max-price");
const priceFormSubmitBtn = document.querySelector(".price-btn");
const pageId = Number(document.querySelector(".page_id").value)
const saleRadioBtn = document.querySelector(".sale-radio");
const rentRadioBtn = document.querySelector(".rent-radio");
const token = document.querySelector("meta[name='token']").getAttribute("content");
const container  = document.querySelector(".ads-container");

//
const profileCirc = document.querySelector(".profile-circle");









const noneFound = `<div class="container p-4 ">

<div class="alert alert-primary d-flex align-items-cente bg-theme" role="alert">
    <i class="bi text-danger bi-exclamation-triangle-fill"></i>
    <div class="p-5">
        No Adds Here
      
    </div>

</div>`





const updateContent  = function(Ads){
    let htmlContent = ""
    Ads.listings.forEach((val) => {
        console.log(val);
        console.log("profile-circ" ,profileCirc)
        htmlContent+= `  <a  class="listing-display  " href="/listing/${val.id} %}">
        <div class="row border mb-3 ">
        
                <div class="col-md-4 ">
                    <div id="carouselExampleControls" class="carousel slide  text-center"  data-bs-interval="false">
                        <div class="carousel-inner">
                            <div class="carousel-item active">
                                <img src="${val.image}" height="200" width="200" alt="image of property">
                            </div>
                       
                        </div>
                      
                    </div> 
                </div>
        
                <div class="col-md-4  col-">
                    <div class="lead title">
                    <div class="product-price">
                        <p><span class="currency">GHC</span>${val.price}</p>
                    </div>
                    <p class="product-description">${val.description}</p>
                    <p class="product-location text-muted">${val.location}</p>

                    <div class="d-inline-flex">
                            ${val.furnished ? ' <h6><span class="  rounded-pill   badge text-bg-secondary">FURSNISHED</span></h6>' :
                            ' <h6><span class=" badge rounded-pill  text-bg-secondary">UNFURNISHED</span></h6>'}
            
                            <h6><span class=" badge rounded-pill mx-1  text-bg-success">${val.accomodation_type}</span></h6>
        
                    </div>
                    
                    </div>

                    ${ profileCirc ?  `<form action="" method="">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${token}">
                    <input hidden value="" name=listing>
                    <button type="submit" class=" fs-6 btn btn-outline-primary"><i class="bi bi-star"></i></button>
                     </form>
                    `: ''}
                      
                </div>  
            
        </div>

    </a>`


    console.log(htmlContent);
    container.innerHTML = htmlContent;
        
    });

}




















 
if(pageId === 1){

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
            container.innerHTML = "";
            
            console.log(result);
            if(result.listings.length  === 0){
                container.innerHTML = noneFound;
            return;

            }

            updateContent(result);
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
            container.innerHTML = "";
            
            console.log(result);
            if(result.listings.length  === 0){
                container.innerHTML = noneFound;
            return;

            }

            updateContent(result);
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
                container.innerHTML = "";
            
            console.log(result);
            if(result.listings.length  === 0){
                container.innerHTML = noneFound;
            return;

            }

            updateContent(result);
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
                container.innerHTML = "";
            
                console.log(result);
                if(result.listings.length  === 0){
                    container.innerHTML = noneFound;
                return;
    
                }
    
                updateContent(result);
            }).catch(error => console.log(error))
    
        }else{
            console.log("ss")
        }
    
    
        
    }

 }
