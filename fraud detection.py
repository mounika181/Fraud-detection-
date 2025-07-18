import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc
from imblearn.under_sampling import RandomUnderSampler
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load and preprocess dataset
file_path = 'creditcard.csv'  # CSV file path
try
    df = pd.read_csv(file_path)
except FileNotFoundError
    raise FileNotFoundError(f❌ File not found {file_path})

df['Amount'] = StandardScaler().fit_transform(df['Amount'].values.reshape(-1, 1))
df = df.drop(['Time'], axis=1)

# 2. Balance data
X = df.drop('Class', axis=1)
y = df['Class']
rus = RandomUnderSampler(random_state=42)
X_res, y_res = rus.fit_resample(X, y)

# 3. Traintest split
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.3, random_state=42)

# 4. Initialize models
models = {
    'Random Forest' RandomForestClassifier(n_estimators=100, random_state=42),
    'Decision Tree' DecisionTreeClassifier(random_state=42),
    'SVM' SVC(kernel='linear', probability=True)
}

# 5. Train and evaluate
accuracies = {}
roc_data = {}
trained_models = {}

for name, model in models.items()
    print(fn🔍 Training {name}...)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[, 1]

    acc = accuracy_score(y_test, y_pred)
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)

    print(f📊 {name} Results)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    print(Accuracy, acc)

    accuracies[name] = acc
    roc_data[name] = (fpr, tpr, roc_auc)
    trained_models[name] = model

# 6. Plot Accuracy Comparison
plt.figure(figsize=(8, 4))
sns.barplot(x=list(accuracies.keys()), y=list(accuracies.values()), palette=viridis)
plt.ylabel(Accuracy)
plt.title(Model Accuracy Comparison)
plt.ylim(0.85, 1.0)
plt.show()

# 7. Plot ROC Curve
plt.figure(figsize=(8, 6))
for name, (fpr, tpr, roc_auc) in roc_data.items()
    plt.plot(fpr, tpr, label=f'{name} (AUC = {roc_auc.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve Comparison')
plt.legend()
plt.grid()
plt.show()

# 8. Mock alert functions
def send_alert_email_and_sms(email, phone, message)
    print(fn📧 Sending Email to {email})
    print(fSubject Fraud Alert Notification)
    print(fBody {message})

    print(fn📱 Sending SMS to {phone})
    print(fMessage {message}n)

# 9. PIN verification simulation
CORRECT_PIN = 1234
MAX_ATTEMPTS = 2

def simulate_transaction(model_name='Random Forest', email='amounik60@gmail.com', phone='7993426100')
    print(n🔐 Transaction Initiated)
    attempts = 0
    while attempts  MAX_ATTEMPTS
        entered_pin = input(Enter your 4-digit PIN )
        if entered_pin == CORRECT_PIN
            print(✅ PIN Verified. Checking transaction with, model_name)
            model = trained_models[model_name]

            # Choose a random legitimate transaction for fairness
            legit_indices = y_test[y_test == 0].index
            random_index = np.random.choice(legit_indices)
            sample = X_test.loc[[random_index]]
            true_label = y_test.loc[random_index]
            prediction = model.predict(sample)[0]

            print(f🎯 Model Prediction {'Fraud' if prediction == 1 else 'Legitimate'})
            print(f🧾 True Label {'Fraud' if true_label == 1 else 'Legitimate'})

            if prediction == 1
                print(🚨 Fraud Detected in transaction!)
                send_alert_email_and_sms(email, phone, Fraudulent transaction detected on your account.)
            else
                print(✅ Transaction is legitimate.)
            return
        else
            attempts += 1
            print(f❌ Incorrect PIN. Attempt {attempts}{MAX_ATTEMPTS})

    print(🚨 Fraud Detected Too many incorrect PIN attempts!)
    send_alert_email_and_sms(email, phone, Multiple incorrect PIN attempts detected on your account!)

# 10. Run transaction simulation
simulate_transaction(model_name='Random Forest')
