"""
File: studentview.py
The view for editing and analyzing student scores.
"""

from breezypythongui import EasyFrame
import matplotlib.pyplot as plt  # For plotting

class StudentView(EasyFrame):

    def __init__(self, model):
        """Creates and lays out window components
        to view and manipulate the model's data."""
        EasyFrame.__init__(self)
        self.setSize(500, 200)
        self.model = model
        self.addLabel("Mean", row=0, column=0)            
        self.addLabel("Median", row=1, column=0)            
        self.addLabel("Mode", row=2, column=0)            
        self.addLabel("Standard deviation", row=3, column=0)
        self.meanFld = self.addFloatField(value=0.0, row=0, column=1, precision=2)            
        self.medianFld = self.addFloatField(value=0.0, row=1, column=1, precision=2)            
        self.modeFld = self.addFloatField(value=0.0, row=2, column=1, precision=1)            
        self.stdFld = self.addFloatField(value=0.0, row=3, column=1, precision=4)                        
        self.addLabel("Data", row=0, column=2, sticky="NEW")
        self.scoreArea = self.addTextArea(text="", row=1, column=2, width=12, rowspan=3)
        
        # Create a panel for the buttons to center them in 5 columns
        bp = self.addPanel(row=4, column=0, columnspan=3, background="black")
        bp.addButton(text="Edit score", row=0, column=0, command=self.editScore)
        bp.addButton(text="Add score", row=0, column=1, command=self.addScore)
        bp.addButton(text="Delete score", row=0, column=2, command=self.deleteScore)
        bp.addButton(text="Randomize scores", row=0, column=3, command=self.randomizeScores)
        bp.addButton(text="Plot scores", row=0, column=4, command=self.plotScores)  # New button
        
        # Place the model's contents in the view
        self.refreshData()

    def refreshData(self):
        """Updates the view with the contents of the model."""
        self.setTitle(self.model.getName() + "'s Scores")
        self.meanFld.setNumber(self.model.getMean())
        self.medianFld.setNumber(self.model.getMedian())
        self.modeFld.setNumber(self.model.getMode())
        self.stdFld.setNumber(self.model.getStd())
        self.scoreArea.setText(str(self.model))

    # Event-handling methods

    def editScore(self):
        """Obtains a new score and its position from the user
        and updates the model and the view."""
        position = self.prompterBox(title="Edit score", promptString="Enter the position of the score to edit:")
        if position is not None:
            try:
                position = int(position)
                if 1 <= position <= len(self.model.scores):
                    new_score = self.prompterBox(title="Edit score", promptString="Enter the new score:")
                    if new_score is not None:
                        self.model.setScore(position, float(new_score))
                        self.refreshData()
                else:
                    self.messageBox(title="Error", message="Invalid position. Please enter a valid position.")
            except ValueError:
                self.messageBox(title="Error", message="Invalid input. Please enter a valid number.")

    def addScore(self):
        """Obtains a new score from the user,
        adds it to the model, and updates the view."""
        new_score = self.prompterBox(title="Add score", promptString="Enter the new score:")
        if new_score is not None:
            try:
                self.model.addScore(float(new_score))
                self.refreshData()
            except ValueError:
                self.messageBox(title="Error", message="Invalid input. Please enter a valid number.")

    def deleteScore(self):
        """Obtains the position of a score from the user,
        deletes the score at that position from the model,
        and updates the view."""
        position = self.prompterBox(title="Delete score", promptString="Position of the score:")
        if position is not None:
            try:
                position = int(position)
                if 1 <= position <= len(self.model.scores):
                    self.model.deleteScore(position)
                    self.refreshData()
                else:
                    self.messageBox(title="Error", message="Invalid position. Please enter a valid position.")
            except ValueError:
                self.messageBox(title="Error", message="Invalid input. Please enter a valid number.")

    def randomizeScores(self):
        """Obtains the number of scores, lowest score,
        and highest score from the user, randomizes the model's scores,
        and updates the view."""
        size = self.prompterBox(title="Randomize scores", promptString="Enter the number of scores:")
        lower = self.prompterBox(title="Randomize scores", promptString="Enter the lowest possible score:")
        upper = self.prompterBox(title="Randomize scores", promptString="Enter the highest possible score:")
        if size is not None and lower is not None and upper is not None:
            try:
                size = int(size)
                lower = int(lower)
                upper = int(upper)
                if size > 0 and lower <= upper:
                    self.model.randomizeScores(size, lower, upper)
                    self.refreshData()
                else:
                    self.messageBox(title="Error", message="Invalid input. Ensure size > 0 and lower <= upper.")
            except ValueError:
                self.messageBox(title="Error", message="Invalid input. Please enter valid numbers.")

    def plotScores(self):
        """Displays a line plot of the student's scores."""
        positions = list(range(1, len(self.model.scores) + 1))  # X-axis: Positions (1, 2, 3, ...)
        scores = self.model.scores  # Y-axis: Scores

        # Create the plot
        plt.figure(figsize=(8, 5))
        plt.plot(positions, scores, marker="o", linestyle="-", color="b")
        plt.title(f"{self.model.getName()}'s Scores")
        plt.xlabel("Position")
        plt.ylabel("Score")
        plt.grid(True)
        plt.xticks(positions)  # Ensure all positions are shown on the x-axis
        plt.show()