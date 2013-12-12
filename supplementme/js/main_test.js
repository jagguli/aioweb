require([
    "dojo/ready",
    "dojo/query",
    "supplementme/main"
], function (ready, query) {
    ready(function () {
        describe("meal widget", function(){
            it("should be visible",
               function(){
                   expect(query('.meals-widget').length).toEqual(1);
                   expect(query('meal-select > option').length).toBeGreaterThan(1);
               });
        });
        describe("on clicking add", function(){
            it("should add selected meal to list of meals",
               function(){
               });
        });
        describe("on clicking save", function(){
            it("should save meal to saved meals",
               function(){
               });
        });
        describe("food widget", function(){
            it("should be visible",
               function(){
                   expect(query('.food-widget').length).toEqual(1);
                   expect(query('meal-select > option').length).toBeGreaterThan(1);
               });
            it("should have nutrients dropdown",
               function(){
                   expect(query('.nutrients-select').length).toEqual(1);
                   expect(query('nutrients-select > option').length).toBeGreaterThan(1);
               });
        });
    });
});
