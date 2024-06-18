%
% This script is useful for visualizing data output (in binary file format)
% from the fortran OceanWave3D model. The script can be easily tailored
% to output data from other data files as well.
%
% The function ShowFreeSurfaceEvolution2D is provided by Allan P. Engsig-Karup, apek@imm.dtu.dk.
% with slight changes from Christian.
% The function 

% Show free surface evolution

function ShowFreeSurfaceEvolution2D(varargin)
    
    curdir = cd;
    
    % Path for data files here
    % dirpath = '/Users/apek/Documents/Fortran/SWENSE3D/bin';
    %dirpath = '/Users/apek/CVS/tests/OleLindberg';
    %dirpath = '/Users/apek/OW3Dtest';
    %dirpath = '/Users/apek/Desktop/OCW3D';

    

    
    
    %
    %************************************************************************
    % *** Set these values to correspond to the run at hand.***
    initialstep = 0;

    [jump, Nsteps, dt, Nx, Ny, plotmethod] = setInputFromInputFile();
    %Nsteps = 1283; %915;
    %jump   = 30;
    %dt     = .0245
    %g      = 9.81;
    %plotmethod = 3;  % 1-> 2D, 2->3D
    Amax=10*50*0.125;%10*50*0.125;       % To set the scale of the z-axis plot
    IOmethod = 1; %0:binary ; 1:classical unformatted ; 2:unformatted ftn95
    fac = 0.05;       %1e-1;
 
    dirpath = [curdir , '/OceanWave3D-Fortran90/docker'];
    cd(dirpath)
    disp(jump);
    %
    %************************************************************************
    
    % CHOOSE BETWEEN byte storage format below (uncomment the one needed)
    % byteorder = 'ieee-be'; % IEEE Big-Endian format 
    byteorder = 'ieee-le'; % IEEE Little-Endian format
    
    for tstep = initialstep : jump : Nsteps
        tid = tstep*dt+dt;
    
        if mod(tstep,10)==0
            disp(sprintf('tstep=%d...',tstep))
        end
    
        switch IOmethod
            case 1 % unformatted file
                fid=fopen(sprintf('EP_%.5d.bin',tstep),'r',byteorder);
                disp(cd);
                disp(sprintf('EP_%.5d.bin',tstep));
                [nrec,count] = fread(fid,1,'int32');
                Nx=fread(fid,1,'int32');
                Ny=fread(fid,1,'int32');
                [nrec,count] = fread(fid,1,'int32');
    
                [nrec,count] = fread(fid,1,'int32');
                X=fread(fid,[Nx Ny],'float64');
                Y=fread(fid,[Nx Ny],'float64');
                [nrec,count] = fread(fid,1,'int32');
    
                [nrec,count] = fread(fid,1,'int32');
                E=fread(fid,[Nx Ny],'float64');
                %                         E=reshape(E(:),nx,ny);
                P=fread(fid,[Nx,Ny],'float64');
                fclose(fid);
             case 2 % unformatted file from ftn95
                fid=fopen(sprintf('EP_%.5d.bin',tstep),'r',byteorder);
                [nrec,count] = fread(fid,1,'int8');
                Nx=fread(fid,1,'int32');
                Ny=fread(fid,1,'int32');
                [nrec,count] = fread(fid,1,'int8');
                if(2*Nx*Ny > 30)
                    [nrec,count] = fread(fid,1,'int8');
                    [nrec,count] = fread(fid,1,'int32');
                    X=fread(fid,[Nx Ny],'float64');
                    Y=fread(fid,[Nx Ny],'float64');
                    [nrec,count] = fread(fid,1,'int32');
                    [nrec,count] = fread(fid,1,'int8');
    
                    [nrec,count] = fread(fid,1,'int8');
                    [nrec,count] = fread(fid,1,'int32');
                    E=fread(fid,[Nx Ny],'float64');
                    %                         E=reshape(E(:),nx,ny);
                    P=fread(fid,[Nx,Ny],'float64');
                    fclose(fid);  
                else
                    [nrec,count] = fread(fid,1,'int8');
                    X=fread(fid,[Nx Ny],'float64');
                    Y=fread(fid,[Nx Ny],'float64');
                    [nrec,count] = fread(fid,1,'int8');
    
                    [nrec,count] = fread(fid,1,'int8');
                    E=fread(fid,[Nx Ny],'float64');
                    %                         E=reshape(E(:),nx,ny);
                    P=fread(fid,[Nx,Ny],'float64');
                    fclose(fid);  
                end  
            otherwise  % binary file
                fid=fopen(sprintf('EP_%.5d.bin',tstep),'r',byteorder);
                Nx=fread(fid,1,'int32');
                Ny=fread(fid,1,'int32');
                X=fread(fid,[Nx Ny],'float64');
                Y=fread(fid,[Nx Ny],'float64');
                E=fread(fid,[Nx Ny],'float64');
                %                         E=reshape(E(:),nx,ny);
                P=fread(fid,[Nx,Ny],'float64');
                fclose(fid);
        end
    %     % time for plotting...
        if Ny==1 | Nx==1
            plotmethod = 1;
        end
    
        switch plotmethod
            case 1
                if Nx>1
     %               plot(X,E,'b')
                                 plot(X,E,'b',X,P,'r')
                    axis([X(1) X(end) -Amax Amax])
                else
                    plot(Y,E,'b') %,Y,P,'r')
                    axis([Y(1) Y(end) -0.1 0.15])
                end
                grid on
            case 2
                %             mesh(X,Y,Eerr*fac)
                %         surf(X,Y,E*fac)
                surf(X(2:end-1,2:end-1),Y(2:end-1,2:end-1),E(2:end-1,2:end-1)*fac)
                colormap(water)
                axis([X(1) X(end) Y(1) Y(end) -0.1 0.1])
                light
                %             axis equal
                axis off
                %             view(0,90)
                % view(-10,0)
            case 3
                subplot(1,3,1)
                mesh(X,Y,E*fac)
                %             axis([x(1) x(end) y(1) y(end) -1 1])
                subplot(1,3,2)
                mesh(X,Y,P*fac)
                %             axis([x(1) x(end) y(1) y(end) -1 1])
                subplot(1,3,3)
                mesh(X,Y,abs(E-P)*fac)
        end
        drawnow
        %hold on
        E'
        pause(0.3)
        % pause
    end
end

% This function is provided by Allan P. Engsig-Karup
function c = water(m)
% WATER Linear blue-tone color map.
% WATER(M) return and M-by-3 matrix containing a "water" colormap.
%
%   WATER, by itself, is the same length as the current colormap.
%
%   For example, to reset the colormap of the current figure:
%
%             colormap(water)
%

if nargin < 1, m = size(get(gcf,'colormap'),1); end
c = min(1,gray(m)*diag([0 1 1-0.5625]));
c(:,3) = c(:,3) + 0.5625;
end


% This function is made by Christian
function [jump, Nsteps, dt, Nx, Ny, plotmethod] = setInputFromInputFile()
    curdir = cd;
    dirpath = [curdir , '/OceanWave3D-Fortran90/docker'];
    cd(dirpath)
    % Open the input file
    fid = fopen('OceanWave3D.inp', 'r');
    if fid == -1
        error('Cannot open the input file.');
    end

    % Initialize NSteps
    Nsteps = 0;
    dt = 0;
    jump = 0;
    Nx = 0;
    Ny = 0;
    plotmethod = 2;
    % Read the file line by line
    tline = fgetl(fid);
    while ischar(tline)
        % Check if the line contains NSteps
        if contains(tline, 'Nsteps') && Nsteps == 0
            % Split the line into parts
            parts = strsplit(tline);
            % Extract the NSteps value
            Nsteps = str2double(parts{1});
            dt = str2double(parts{2});
        elseif contains(tline, 'StoreDataOnOff') && jump == 0
            % Split the line into parts
            parts = strsplit(tline);
            jump = abs(str2double(parts{1}));
        elseif contains(tline, 'Ny') && Ny == 0
            % Split the line into parts
            parts = strsplit(tline);
            Nx = abs(str2double(parts{4}));
            Ny = abs(str2double(parts{5}));
            if Ny==1 | Nx==1
                plotmethod = 1;
            end
        end
        
        % Read the next line
        tline = fgetl(fid);
    end
    
    % Close the file
    fclose(fid);
    
    % Check if Nsteps was found
    if isempty(Nsteps)
        error('Nsteps not found in the input file.');
    end
    
end
