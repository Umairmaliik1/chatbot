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

              advancedSettings: function () {
              },

              destroy: function(){              
              },    

              contacts: { selected: function() {                  
                    }
              },

              onSalesbotDesignerSave: function (handler_code, params) {
                    const hookUrl = params?.text || '';

                    // Data we want to send to your server on every inbound message:
                    const requestData = {
                      from: 'widget',
                      // message_text comes from the previous step (Incoming message)
                      message: '{{message_text}}',
                      chat_id: '{{chat_id}}',
                      lead_id: '{{lead.id}}',
                      visitor_id: '{{visitor.id}}'
                    };

                    const firstStep = {
                      question: [
                        {
                          handler: 'widget_request',
                          params: {
                            url: hookUrl,
                            data: requestData
                          }
                        }
                      ],
                      require: []
                    };

                    const flow = [firstStep];
                    return JSON.stringify(flow);
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
