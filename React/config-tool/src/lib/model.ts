type Phase = {
    id: string; // Unique phase ID
    name: string; // Phase name
}

type Factor = {
    id: string; // Unique factor ID
    name: string; // Factor name
    attributes: string[]; // Attributes of the factor
}

class Outcome {
    name: string;  // Outcome name

    constructor() {
        this.name = "";
    }


}

class Model {
    phases: Phase[];
    factors: Factor[];
    outcomes: Outcome[];

    constructor() {
        this.phases = [];
        this.factors = [];
        this.outcomes = [];
    }

    debug() {
        console.log(`Phases:`);
        console.table(this.phases);
        console.log(`Factors:`);
        console.table(this.factors);
    }

    // -------------------------------------------------------------------------
    // CRUD operations on phases
    // -------------------------------------------------------------------------

    private phaseIndexExists(index: number):boolean {
        return index >= 0 && index < this.phases.length
    }

    // Create a new (blank) phase.
    newPhase() {
        this.addPhase("", "");
    }

    // Add a phase to the model.
    addPhase(id: string, name: string) {
        this.phases.push({id, name});
    }

    // Delete a phase from the model given its index.
    deletePhase(index: number) {
        if (!this.phaseIndexExists(index)) {
            console.error(`Can't delete phase with index ${index}`);
        }
        this.phases.splice(index, 1);
    }

    // Update the ID of a phase given its index.
    updatePhaseId(index: number, newId: string) {
        if (!this.phaseIndexExists(index)) {
            console.error(`Can't update phase ID for index ${index}`);
            return;
        }
        this.phases[index].id = newId;
    }

    // Update the name of a phase given its index.
    updatePhaseName(index: number, newName: string) {
        if (!this.phaseIndexExists(index)) {
            console.error(`Can't update phase name for index ${index}`);
            return;
        }        
        this.phases[index].name = newName;
    }

    // -------------------------------------------------------------------------
    // CRUD operations on factors
    // -------------------------------------------------------------------------

    private factorIndexExists(index: number):boolean {
        return index >= 0 && index < this.factors.length
    }

    newFactor() {
        this.addFactor("", "", []);
    }

    // Add a factor to the model.
    addFactor(id: string, name: string, attributes: string[]) {
        this.factors.push(({
            id,
            name,
            attributes
        }));
    }

    // Delete a factor from the model given its index.
    deleteFactor(index: number) {
        if (!this.factorIndexExists(index)) {
            console.error(`Can't delete factor with index ${index}`);
        }
        this.factors.splice(index, 1);
    }

    // Update the ID of a factor given its index.
    updateFactorId(index: number, newId: string) {
        if (!this.factorIndexExists(index)) {
            console.error(`Can't update factor ID with index ${index}`);
        }
        this.factors[index].id = newId;
    }

    // Update the name of a factor given its index.
    updateFactorName(index: number, newName: string) {
        if (!this.factorIndexExists(index)) {
            console.error(`Can't update factor name with index ${index}`);
        }
        this.factors[index].name = newName;        
    }

    // Update the attributes of a factor given its index.
    updateFactorAttributes(index: number, newAttributes: string[]) {
        if (!this.factorIndexExists(index)) {
            console.error(`Can't update factor attributes with index ${index}`);
        }
        this.factors[index].attributes = newAttributes;
    }

    // -------------------------------------------------------------------------
    // CRUD operations on outcomes
    // -------------------------------------------------------------------------
    
    newOutcome() {
        this.outcomes.push(new Outcome());
    }
}

export default Model;