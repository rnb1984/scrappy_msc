 var app = angular.module("myApp", ["ngRoute"]);

// routers for urls
app.config(function($routeProvider) {
    $routeProvider
    .when("/", {
        templateUrl : "/pizza_face/templates/main.htm",
    })
    .when("/details", {
        templateUrl : "/pizza_face/templates/details.htm",
    })
    .when("/pizzas", {
        templateUrl : "/pizza_face/templates/pizzas.htm",
    })
    .when("/prediction", {
        templateUrl : "/pizza_face/templates/prediction.htm",
    });
});

// controller functions      
app.controller('pizzaChoice', function($scope) {
    
    
    $scope.pizzas = [
        {name :'Pizza pasta salad', image : 'http://www.bbcgoodfood.com/sites/default/files/styles/recipe/public/recipe_images/pasta_1.jpg?itok=YHYg0NS_', ingredients : [
            {name : 'salami', amout : '1'},
            {name : 'olives', amout : '1'},
            {name : 'Basil', amout : '1'},
            {name : 'pasta', amout : '1'},
            {name : 'olive oil', amout : '1'}
            ]
        },
        {name :'Brie & potato pizza', image : 'http://www.bbcgoodfood.com/sites/default/files/styles/recipe/public/recipe_images/recipe-image-legacy-id--511_12.jpg?itok=yK1ADXxX', ingredients : [
            {name : 'Brie', amout : '1'},
            {name : 'potato', amout : '1'},
            {name : 'rosemary', amout : '1'},
            {name : 'olives', amout : '1'},
            {name : 'olive oil', amout : '1'}
            ]
        },
        {name :'Potato & taleggio pizza', image : 'http://www.bbcgoodfood.com/sites/default/files/styles/recipe/public/recipe_images/recipe-image-legacy-id--3903_10.jpg?itok=7RZgVpTn', ingredients : [
            {name : 'Taleggio', amout : '1'},
            {name : 'new potato', amout : '1'},
            {name : 'spring onion', amout : '1'}
            ]
        }
    ]
    
    
    });