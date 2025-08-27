define(['jquery'], function($){
  let CustomWidget = function () {
        let self = this, // to access an object from methods
        system = self.system(), // this method returns an object with system variables.
        langs = self.langs;  // localization object with data from the localization file (i18n folder)
       
        this.callbacks = {
              settings: function(){
              },

              init: function(){      
                    return true;
              },

              bind_actions: function(){        
                    return true;
              },

              render: function(){      
                    return true;
              },    

              dpSettings: function(){              
              },

              advancedSettings: function() {
              },

              destroy: function(){              
              },    

              contacts: { selected: function() {                  
                    }
              },

              onSalesbotDesignerSave: function (handler_code, params) {
              },

              leads: { selected: function() {                  
                    }
              },

              todo: { selected: function () {}
              },

              onSave: function () {},
              
              onAddAsSource: function (pipeline_id) {}
              };
        return this;
    };
  return CustomWidget;
});