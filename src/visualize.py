import matplotlib.pyplot as plt

def plot_predictions(y_test, preds):
    plt.figure(figsize=(10,5))
    plt.plot(y_test.values, label='Actual')
    plt.plot(preds, label='Predicted')
    plt.legend()
    plt.title("Prediction vs Actual")
    plt.show()