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
const postListingForm = document.querySelector(".post-form");
const postListingFormSpinner = document.querySelector(".post-spinner");
const imagePick = document.querySelector(".image-picker");
const imagePreview = document.querySelector(".image-preview");
const profileImagePreview = document.querySelector(".profile-image-preview");
const profileImagePick = document.querySelector(".profile-picker")



//
const profileCirc = document.querySelector(".profile-circle");
const starBtns = document.querySelectorAll(".star-button");


console.log(starBtns);







//functions
const starPost = function(ele){
    console.log(ele.innerHTML)
    
    fetch("/stared",{
        method:"POST",
        headers:{"X-CSRFToken":token},
        body:JSON.stringify({
            id:ele.dataset.id,
        })
    }).then(response => response.json()).then(result => {
        console.log(result)
        if(result.status === "ok"){
            if (ele.innerHTML == '<i class="bi bi-star"></i>'){
                console.log("here");
                ele.innerHTML = "<i class='bi bi-star-fill'></i>"
                
            }else{
                console.log("here rather");
                ele.innerHTML = "<i class='bi bi-star'></i>"
            }
        }
    }).catch(error => {
        console.log(error)
    })
}



const styleImage = function(image){
    image.style.marginRight ="20px";
    image.style.width = "100px";

}



starBtns.forEach(val => {
    val.addEventListener("click", function(e){
        e.preventDefault(e);
        starPost(this);
    })
})






const noneFound = `<div class="container p-4 ">
<div class="alert alert-primary d-flex align-items-cente bg-theme" role="alert">
    <i class="bi text-danger bi-exclamation-triangle-fill"></i>
    <div class="p-5">
        No Adds Here
      
    </div>

</div>`





const updateContent  = function(Ads){
    let htmlContent = "";
    Ads.listings.forEach((val) => {
        htmlContent+= `  <a  class="listing-display  " href="/listing/${val.id}">
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

                     ${Ads.favs.includes(val.id) ? `<button type="submit" class=" fs-6 btn btn-outline-primary"><i class="bi bi-star-fill"></i></button>
                     </form>` : ` <button type="submit" class=" fs-6 btn btn-outline-primary"><i class="bi bi-star"></i></button>
                     </form>`}
                   

                    `: ''}
                      
                </div>  
            
        </div>

    </a>`
        
    });

    container.innerHTML = htmlContent;    

}
























//driver
 
if(pageId === 1){
    const usr = Number(document.querySelector(".userid").value)

    const renderResults = function(result){
       
        if(result.listings.length  === 0){
            container.innerHTML = noneFound;
        return;
        }

        updateContent(result);

    }

    const showSpinner = function(){
        container.innerHTML = `<div class="text-center mt-5 fs-2 text-success">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>`;
        
    }




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

        showSpinner();
        
    
        fetch("/home/page/1",{
            method:"POST",
            headers:{"X-CSRFToken":token},
            body:JSON.stringify({
                action:"price_filter",
                user:usr,
                min_price:min,
                max_price:max
            })
        }).then(response => response.json()).then( result => {
    
            ///////////TODO
            renderResults(result)

        })
        .catch(error => console.log(error))
    
        
    }
    
    
    
    
    
    
    locationSelect.onchange = function(e){

       showSpinner();
        
        fetch("/home/page/1",{
            method:"POST",
            headers:{"X-CSRFToken":token},
            body:JSON.stringify({
                action:"location_filter",
                user:usr,
                location:this.value
            })
        }).then(response => response.json()).then(result =>{
    
            //////////////TODO
            renderResults(result)
        }).catch(error => console.log(error))
    }
    
    
    
    
    
    
    saleRadioBtn.onchange = function(e){
        if(this.checked = true){
            if(rentRadioBtn.checked = true) rentRadioBtn.checked = false;

            showSpinner();
            
    
            fetch("/home/page/1",{
                method:"POST",
                headers:{"X-CSRFToken":token},
                body:JSON.stringify({
                    action:"sale_filter",
                    user:usr
                })
            }).then(response => response.json()).then(result => {
    
                ///TODO
                    renderResults(result)

            }).catch(error => console.log(error))
    
        }else{
            console.log("ss")
        }
    
    
        
    }
    
    
    
    

    
    rentRadioBtn.onchange = function(e){
        if(this.checked = true){
            if(saleRadioBtn.checked = true) saleRadioBtn.checked = false;

            showSpinner();
    
            fetch("/home/page/1",{
                method:"POST",
                headers:{"X-CSRFToken":token},
                body:JSON.stringify({
                    action:"rent_filter",
                    user:usr
                })
            }).then(response => response.json()).then(result => {
    
                ////TODO
                    renderResults(result)
            }).catch(error => console.log(error))
    
        }else{
            console.log("ss")
        }
    
    
        
    }

}


























if (pageId == 2){
    postListingForm.onsubmit = function(){
        postListingFormSpinner.innerHTML = `   <div class="text-center text-success">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
    </div>`;
    }



    imagePick.onchange = function(){
        imagePreview.style.display = "block"
        imagePreview.innerHTML = "";
        const files = [...this.files]
        files.forEach( val => {
            const img = new Image();
            img.src = URL.createObjectURL(val);
            styleImage(img);
            imagePreview.append(img);
        })   
    }
}













if(pageId == 4){
    profileImagePick.onchange = function(){
        profileImagePreview.style.display ="block";
        profileImagePreview.innerHTML = "";
        const img = new Image();
        img.src = URL.createObjectURL(this.files[0])
        styleImage(img)
        profileImagePreview.append(img)
        
    }

}