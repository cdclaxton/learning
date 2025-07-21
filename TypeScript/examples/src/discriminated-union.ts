interface Cat {
    kind: "cat";
    sound: string;
}

interface Dog {
    kind: "dog";
    happySound: string;
}

type Animal = Cat | Dog;

// interface Frog {
//     kind: "frog";
//     sound: "ribbit";
// }

// type Animal = Cat | Dog | Frog;

function makeSound(a: Animal): string {
    switch (a.kind) {
        case "cat":
            return a.sound;
        case "dog":
            return a.happySound;
        default:
            // Type 'Frog' is not assignable to type 'never'.ts(2322)
            const _exhaustiveCheck: never = a;
            return _exhaustiveCheck;
    }
}

makeSound({
    kind: "cat",
    sound: "meow",
});