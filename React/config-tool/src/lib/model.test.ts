import Model from "./model";

test('initialise model', () => {
    const model = new Model();
    expect(model.phases).toHaveLength(0);
    expect(model.factors).toHaveLength(0);
    expect(model.outcomes).toHaveLength(0);
});

test('new phase', () => {
    const model = new Model();
    model.newPhase();
    expect(model.phases).toHaveLength(1);    
})

test('add a phase', () => {
    const model = new Model();

    // Add the first phase
    const phaseId1 = "phase-1-id";
    const phaseName1 = "phase-1-name";

    model.addPhase(phaseId1, phaseName1);
    expect(model.phases).toStrictEqual([{
        id: phaseId1,
        name: phaseName1,
    }]);

    // Add the second phase
    const phaseId2 = "phase-2-id";
    const phaseName2 = "phase-2-name";

    model.addPhase(phaseId2, phaseName2);
    expect(model.phases).toStrictEqual([
    {
        id: phaseId1,
        name: phaseName1,
    },
    {
        id: phaseId2,
        name: phaseName2,
    }]);   
});

test('delete a phase', () => {
    const model = new Model();

    // Add the first phase
    const phaseId1 = "phase-1-id";
    const phaseName1 = "phase-1-name";
    model.addPhase(phaseId1, phaseName1);

    // Add the second phase
    const phaseId2 = "phase-2-id";
    const phaseName2 = "phase-2-name";
    model.addPhase(phaseId2, phaseName2);

    // Add the third phase
    const phaseId3 = "phase-3-id";
    const phaseName3 = "phase-3-name";
    model.addPhase(phaseId3, phaseName3);

    expect(model.phases).toStrictEqual([
    {
        id: phaseId1,
        name: phaseName1,
    },
    {
        id: phaseId2,
        name: phaseName2,
    },
    {
        id: phaseId3,
        name: phaseName3,
    }]);

    // Delete the first phase
    model.deletePhase(0);
    expect(model.phases).toStrictEqual([
    {
        id: phaseId2,
        name: phaseName2,
    },
    {
        id: phaseId3,
        name: phaseName3,
    }]);
    
    // Delete the third phase
    model.deletePhase(1);
    expect(model.phases).toStrictEqual([
    {
        id: phaseId2,
        name: phaseName2,
    }]);
});

test('update the ID and name of a phase', () => {
    const model = new Model();

    // Add the first phase
    const phaseId1 = "phase-1-id";
    const phaseName1 = "phase-1-name";
    model.addPhase(phaseId1, phaseName1);

    // Add the second phase
    const phaseId2 = "phase-2-id";
    const phaseName2 = "phase-2-name";
    model.addPhase(phaseId2, phaseName2);

    // Update the ID of the second phase
    model.updatePhaseId(1, "phase-2-id-new");
    expect(model.phases).toStrictEqual([
    {
        id: phaseId1,
        name: phaseName1,
    },
    {
        id: "phase-2-id-new",
        name: phaseName2,
    }]);
    
    // Update the name of the first phase
    model.updatePhaseName(0, "phase-1-name-new");
    expect(model.phases).toStrictEqual([
    {
        id: phaseId1,
        name: "phase-1-name-new",
    },
    {
        id: "phase-2-id-new",
        name: phaseName2,
    }]);    
});

test('new factor', () => {
    const model = new Model();
    model.newFactor();
    expect(model.factors).toHaveLength(1);
})

test('add a factor', () => {
    const model = new Model();

    // Add the first factor
    model.addFactor("id-1", "name-1", ["a-1", "a-2"]);
    expect(model.factors).toStrictEqual([
        {
            id: "id-1",
            name: "name-1",
            attributes: ["a-1", "a-2"]
        }
    ])

    // Add the second factor
    model.addFactor("id-2", "name-2", []);
    expect(model.factors).toStrictEqual([
        {
            id: "id-1",
            name: "name-1",
            attributes: ["a-1", "a-2"]
        },
        {
            id: "id-2",
            name: "name-2",
            attributes: []
        }
    ])    
});

test('delete a factor', () => {
    const model = new Model();
    model.addFactor("id-1", "name-1", ["a-1", "a-2"]);
    model.addFactor("id-2", "name-2", []);

    model.deleteFactor(1);
    expect(model.factors).toStrictEqual([
        {
            id: "id-1",
            name: "name-1",
            attributes: ["a-1", "a-2"]
        }
    ]);

    model.deleteFactor(0);
    expect(model.factors).toHaveLength(0);
});

test('update the ID of a factor', () => {
    const model = new Model();
    model.addFactor("id-1", "name-1", ["a-1", "a-2"]);
    model.addFactor("id-2", "name-2", []);

    model.updateFactorId(1, "id-2-new");
    expect(model.factors).toStrictEqual([
        {
            id: "id-1",
            name: "name-1",
            attributes: ["a-1", "a-2"]
        },
        {
            id: "id-2-new",
            name: "name-2",
            attributes: []
        }
    ]);    
});

test('update the name of a factor', () => {
    const model = new Model();
    model.addFactor("id-1", "name-1", ["a-1", "a-2"]);
    model.addFactor("id-2", "name-2", []);

    model.updateFactorName(1, "name-2-new");
    expect(model.factors).toStrictEqual([
        {
            id: "id-1",
            name: "name-1",
            attributes: ["a-1", "a-2"]
        },
        {
            id: "id-2",
            name: "name-2-new",
            attributes: []
        }
    ]);    
});

test('update the attributes of a factor', () => {
    const model = new Model();
    model.addFactor("id-1", "name-1", ["a-1", "a-2"]);
    model.addFactor("id-2", "name-2", []);
    
    model.updateFactorAttributes(1, ["b-1", "b-2"]);
    expect(model.factors).toStrictEqual([
        {
            id: "id-1",
            name: "name-1",
            attributes: ["a-1", "a-2"]
        },
        {
            id: "id-2",
            name: "name-2",
            attributes: ["b-1", "b-2"]
        }
    ]);
});

test('new outcome', () => {
    const model = new Model();
    model.newOutcome();
    expect(model.outcomes).toHaveLength(1);
});