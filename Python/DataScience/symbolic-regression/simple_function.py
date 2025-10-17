from pysr import PySRRegressor
import numpy as np

if __name__ == "__main__":

    # Random X points (100 x 5 matrix), i.e. 100 points with
    # 5 features
    X = 2 * np.random.randn(100, 5)

    # y = 2.5382 cos(x_3) + x_0^2 - 0.5
    y = 2.5382 * np.cos(X[:, 3]) + X[:, 0] ** 2 - 0.5

    model = PySRRegressor(
        maxsize=20,
        niterations=40,
        binary_operators=["+", "*"],
        unary_operators=[
            "cos",
            "sin",
            "exp",
            "inv(x) = 1/x",
        ],
        extra_sympy_mappings={"inv": lambda x: 1 / x},
        elementwise_loss="loss(prediction, target) = (prediction - target)^2",
    )

    # Train the model
    model.fit(X, y)

    # Print the learned equations
    print(model)

    #
    print(model.get_best())
