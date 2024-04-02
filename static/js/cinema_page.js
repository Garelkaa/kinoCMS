document.getElementById("inputGroupFileAddon01").addEventListener("click", function() {
        document.getElementById("inputGroupFile01").click();
    });

    document.getElementById("inputGroupFile01").addEventListener("change", function(event) {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = function(e) {
            document.getElementById("mainImage").src = e.target.result;
        }

        reader.readAsDataURL(file);
    });

    function deleteImage() {
        document.getElementById("mainImage").src = "";
    }

    document.getElementById("inputGroupFileAddon02").addEventListener("click", function() {
        document.getElementById("inputGroupFile02").click();
    });

    document.getElementById("inputGroupFile02").addEventListener("change", function(event) {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = function(e) {
            document.getElementById("topImage").src = e.target.result;
        }

        reader.readAsDataURL(file);
    });

    function deleteTopImage() {
        document.getElementById("topImage").src = "";
    }