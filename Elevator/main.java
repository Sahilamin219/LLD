package Elevator;
/* 
Requirements:
1. System manages 3 elevators serving 10 floors (0-9)
2. Users can request an elevator from any floor (hall call). System decides which elevator to dispatch.
3. Once inside, users can select one or more destination floors
4. Simulation runs in discrete time steps (e.g., a `step()` or `tick()` call advances time)
5. Elevator stops come in two types:
    - Hall calls: Request from a floor with direction (UP or DOWN)
    - Destination: Request from inside elevator (no direction specified)
6. System handles multiple concurrent pickup requests across floors
7. Invalid requests should be rejected (return false)
    - Non-existent floor numbers
8. Requests for the current floor are treated as a no-op / already served (doors out of scope)

Out of scope:
- Weight capacity and passenger limits
- Door open/close mechanics
- Emergency stop functionality
- Dynamic floor/elevator configuration
- UI/rendering layer
*/



/*  
ElevetorController : 
    - elevevators[];
    - floors;

    + dipatchElevator(floor, direction) : Elevator
    + requestDestination(elevatorId, floor) : boolean
    + step() : void
    

Elevator:
    - id
    - currentFloor
    - direction (UP, DOWN, IDLE)
    - destinationQueue

    + move() : void

*/

import java.util.ArrayList;
import java.util.List;

class Elevator {
    int id;
    int currentFloor;
    String direction;
    List<Integer> destinationQueue;

    public Elevator(int id) {
        this.id = id;
        this.currentFloor = 9;
        this.direction = "IDLE";
        this.destinationQueue = new ArrayList<>();
    }
}


class ElevatorController {
    private static ElevatorController instance;
    List<Elevator> elevators;
    int numFloors;


    public ElevatorController(int numElevators, int numFloors) {
        this.numFloors = numFloors;
        this.elevators = new ArrayList<>();
        for (int i = 0; i < numElevators; i++) {
            elevators.add(new Elevator(i));
        }
    }

    public static ElevatorController getInstance(int numElevators, int numFloors) {
        if (instance == null) {
            instance = new ElevatorController(numElevators, numFloors);
        }
        return instance;
    }
    
    public void step() {

        for (Elevator elevator : elevators) {

            if (!elevator.destinationQueue.isEmpty()) {
                int nextFloor = elevator.destinationQueue.get(0);
                if (elevator.currentFloor < nextFloor) {
                    elevator.currentFloor++;
                } else if (elevator.currentFloor > nextFloor) {
                    elevator.currentFloor--;
                }

                if (elevator.currentFloor == nextFloor) {
                    System.out.println("Elevator " + elevator.id + " reached floor " + nextFloor);
                    elevator.destinationQueue.remove(0); // Remove served destination
                    
                    if (!elevator.destinationQueue.isEmpty()) {
                        System.out.println("Elevator " + elevator.id + " now serving " + elevator.destinationQueue.get(0));
                        updateDirection(elevator); // Update direction after serving
                    } else {
                        elevator.direction = "IDLE"; // No more destinations, set to IDLE
                    }
                }
            } else {
                elevator.direction = "IDLE"; // No destinations, set to IDLE
            }
        }
        // Simulate time step (1 second) after all elevators have moved
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt(); // Restore interrupted status (better than printStackTrace)
        }
    }

    public boolean requestDestination(int elevatorId, int DestinationFloor) {
        if (elevatorId < 0 || elevatorId >= elevators.size() || DestinationFloor < 0 || DestinationFloor >= numFloors) {
            return false; // Invalid request
        }

        
        Elevator elevator = elevators.get(elevatorId);
        if (!elevator.destinationQueue.contains(DestinationFloor)) { // Avoid duplicate requests or destination same as current floor
            elevator.destinationQueue.add(DestinationFloor); // 0->5 1 -> 2
            updateDirection(elevator);
        }
        return true;
        // ele 1 : 9
        // usrr[0,1,3]
        // dest[5,2,6]
    }



    public Elevator dispatchElevator(String direction, int currFloor) {
        // Validate request
        if (currFloor < 0 || currFloor >= numFloors || (!direction.equals("UP") && !direction.equals("DOWN"))) {
            return null; // Invalid request
        }

        // Find the best elevator to dispatch
        Elevator bestElevator = null;
        int bestScore = Integer.MAX_VALUE;

        for (Elevator elevator : elevators) {
            int score = calculateScore(elevator, currFloor, direction);
            if (score < bestScore) {
                bestScore = score;
                bestElevator = elevator;
            }
        }

        if (bestElevator != null) {
            bestElevator.destinationQueue.add(currFloor); //[0,1]
            updateDirection(bestElevator);
        }

        return bestElevator;
    }

    void updateDirection(Elevator elevator) {
        if (elevator.destinationQueue.isEmpty()) { // 5 -> 2 -> queue is empty after serving 5, then direction should be IDLE
            elevator.direction = "IDLE";
        } else if (elevator.currentFloor < elevator.destinationQueue.get(0)) { // curr2. elevatordest 5.
            elevator.direction = "UP";
        } else if (elevator.currentFloor > elevator.destinationQueue.get(0)) { // curr 2. elevatordest 0.
            elevator.direction = "DOWN";
        }
    }

    int calculateScore(Elevator elevator, int currFloor, String direction) {
        int distanceScore = Math.abs(elevator.currentFloor - currFloor);
        int queueScore = elevator.destinationQueue.size() * 100; // Penalize busy elevators

        if (elevator.direction.equals("IDLE")) {
            // IDLE elevators are preferred: lower score
            return distanceScore + queueScore;
        } else if (elevator.direction.equals(direction)) {
            // Same direction: good candidate if on the way
            if ((direction.equals("UP") && elevator.currentFloor <= currFloor) ||
                (direction.equals("DOWN") && elevator.currentFloor >= currFloor)) {
                return distanceScore + queueScore;
            }
        }
        // Not a good candidate
        return Integer.MAX_VALUE;
    }

    
}





public class main {
    public static void main(String[] args) {
        ElevatorController controller = ElevatorController.getInstance(3, 10);
        
        // Example requests
        Elevator e1 = controller.dispatchElevator("UP", 0);
        Elevator e2 = controller.dispatchElevator("UP", 1);
        boolean result1 = controller.requestDestination(e1.id, 9);
        boolean result2 = controller.requestDestination(e2.id, 5);

        // Simulate 10 time steps
        for (int i = 0; i < 30; i++) {
            controller.step(); // Moves elevators, sleeps 1s
            System.out.println("Step " + (i + 1) + ": Elevator 0 at " + controller.elevators.get(0).currentFloor + " state: " + controller.elevators.get(0).direction +
                           ", Elevator 1 at " + controller.elevators.get(1).currentFloor+ " state: " + controller.elevators.get(1).direction);
        }
    }
}