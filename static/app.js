$(async function () {

 
    
    function generateCupcakeHTML(cupcake) {
        const cupcakeMarkup = $(`
            <div class="card p-3" style="width: 18rem;">
                <img src="${cupcake.image}" class="card-img-top" alt="${cupcake.flavor}">
                <div class="card-body">
                <h5 class="card-title">${cupcake.flavor}</h5>
                <p class="card-text">Size: ${cupcake.size}</p>
                <p class="card-text">Rating: ${cupcake.rating}</p>
                </div>
            </div>
        `);
        return cupcakeMarkup;
    }

    async function getCupcakes() {
        let responce = await axios.get("/api/cupcakes");
        return responce.data.cupcakes;
    };
    
    async function generateCupcakes() {
        const cupcakes = await getCupcakes();
        for (let cupcake of cupcakes) {
            let cake = generateCupcakeHTML(cupcake);
            $("#all-cupcakes").append(cake);
        }
    }

    $("#ccform").on("submit", async function (e) {
        e.preventDefault();

        let flavor = $('#ccflavor').val();
        let size = $('#ccsize').val();
        let rating = $('#ccrating').val();
        let image = $('#ccimg-link').val();

        console.log(flavor, size, rating, image);


        let ccresp = await axios.post('/api/cupcakes', {flavor, size, rating, image});
        let newcupecake = $(generateCupcakeHTML(ccresp.data.cupcake));

        $('#all-cupcakes').append(newcupecake);
        $('#ccform').trigger('reset');
    })

    generateCupcakes();


});