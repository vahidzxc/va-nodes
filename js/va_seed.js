import { app } from "../../../scripts/app.js";

const SEED_MAX = Math.pow(2, 40);

app.registerExtension({
    name: "va.seed",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "VA_Seed") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated?.apply(this, arguments);
                
                const randomButton = this.addWidget(
                    "button", 
                    "🎲", 
                    null, 
                    () => this.generateRandomSeed()
                );
                
                randomButton.serialize = false;
                return r;
            };
            
            nodeType.prototype.generateRandomSeed = function() {
                const seedWidget = this.widgets.find(w => w.name === "seed");
                const previousSeedWidget = this.widgets.find(w => w.name === "previous_seed");
                
                if (seedWidget && previousSeedWidget) {
                    previousSeedWidget.value = seedWidget.value;
                    seedWidget.value = Math.floor(Math.random() * SEED_MAX);
                    this.force_run = true;  // فعال کردن force_run
                    app.queuePrompt();
                }
            };
        }
    }
});